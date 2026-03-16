#!/usr/bin/env python3

import socket
import subprocess
import platform
import ipaddress
import threading
import csv
import json
from concurrent.futures import ThreadPoolExecutor

# Tentative import scapy
try:
    from scapy.all import ARP, Ether, srp
    HAS_SCAPY = True
except:
    HAS_SCAPY = False


class NetworkScanner:

    def __init__(self):

        self.system = platform.system().lower()
        self.results = []
        self.lock = threading.Lock()

    # -------------------------
    # Détection IP locale
    # -------------------------

    def get_local_network(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        local_ip = s.getsockname()[0]

        s.close()

        network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)

        return str(network)

    # -------------------------
    # Ping host
    # -------------------------

    def ping_host(self, ip):

        if self.system == "windows":
            cmd = ["ping", "-n", "1", "-w", "500", ip]
        else:
            cmd = ["ping", "-c", "1", "-W", "1", ip]

        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        return result.returncode == 0

    # -------------------------
    # Hostname
    # -------------------------

    def get_hostname(self, ip):

        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Inconnu"

    # -------------------------
    # MAC Address
    # -------------------------

    def get_mac(self, ip):

        if not HAS_SCAPY:
            return "N/A"

        try:

            arp = ARP(pdst=ip)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")

            packet = ether / arp

            result = srp(packet, timeout=1, verbose=False)[0]

            for sent, received in result:
                return received.hwsrc

        except:
            pass

        return "N/A"

    # -------------------------
    # Scan ports
    # -------------------------

    def scan_ports(self, ip, ports=[21,22,23,25,53,80,110,139,143,443,445,3389]):

        open_ports = []

        for port in ports:

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.settimeout(0.5)

            result = sock.connect_ex((ip, port))

            if result == 0:
                open_ports.append(port)

            sock.close()

        return open_ports

    # -------------------------
    # Scan réseau
    # -------------------------

    def scan_network(self, network):

        network_obj = ipaddress.IPv4Network(network)

        active_ips = []

        print(f"\nScan du réseau {network}")

        def worker(ip):

            if self.ping_host(str(ip)):

                with self.lock:
                    active_ips.append(str(ip))

        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(worker, network_obj.hosts())

        print(f"Machines actives détectées : {len(active_ips)}\n")

        for ip in active_ips:

            hostname = self.get_hostname(ip)

            mac = self.get_mac(ip)

            ports = self.scan_ports(ip)

            self.results.append({
                "ip": ip,
                "hostname": hostname,
                "mac": mac,
                "ports": ports
            })

        self.results.sort(key=lambda x: ipaddress.IPv4Address(x["ip"]))

    # -------------------------
    # Affichage
    # -------------------------

    def display(self):

        print("\nRESULTATS\n")

        print("{:<16} {:<25} {:<18} {}".format(
            "IP", "HOSTNAME", "MAC", "PORTS OUVERTS"))

        print("-"*80)

        for r in self.results:

            ports = ",".join(map(str, r["ports"])) if r["ports"] else "-"

            print("{:<16} {:<25} {:<18} {}".format(
                r["ip"],
                r["hostname"],
                r["mac"],
                ports
            ))

    # -------------------------
    # Export CSV
    # -------------------------

    def export_csv(self):

        with open("scan_reseau.csv", "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow(["IP","Hostname","MAC","Ports"])

            for r in self.results:

                writer.writerow([
                    r["ip"],
                    r["hostname"],
                    r["mac"],
                    ",".join(map(str,r["ports"]))
                ])

        print("\nExport CSV : scan_reseau.csv")

    # -------------------------
    # Export JSON
    # -------------------------

    def export_json(self):

        with open("scan_reseau.json","w",encoding="utf-8") as f:

            json.dump(self.results,f,indent=4)

        print("Export JSON : scan_reseau.json")


# -------------------------
# MAIN
# -------------------------

def main():

    scanner = NetworkScanner()

    network = scanner.get_local_network()

    print("Réseau détecté :", network)

    scanner.scan_network(network)

    scanner.display()

    scanner.export_csv()

    scanner.export_json()

    print("\nScan terminé :", len(scanner.results),"machines")


if __name__ == "__main__":
    main()