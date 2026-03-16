# 🔒 Network Scanner Python

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![GitHub Workflow](https://img.shields.io/github/actions/workflow/status/TON_USERNAME/TON_REPO/python-app.yml?branch=main)
![PyPI Version](https://img.shields.io/pypi/v/your-package-name?color=orange)
![CodeQL](https://img.shields.io/github/dependabot/TON_USERNAME/TON_REPO?logo=github&color=yellow)
![Last Commit](https://img.shields.io/github/last-commit/TON_USERNAME/TON_REPO)

---

## 🚀 Description

**Network Scanner Python** est un outil avancé pour **scanner les réseaux locaux** et détecter les machines actives.  
Idéal pour l’apprentissage en cybersécurité, pentesting interne et audits réseau.

Il permet de :

- Identifier les IP et hostnames
- Détecter les adresses MAC (ARP)
- Scanner les ports courants (SSH, Telnet, HTTP, HTTPS, SMB…)
- Exporter les résultats en **CSV** et **JSON**
- Générer un exécutable `.exe` pour Windows

---

## ⚙️ Fonctionnalités

- ✅ Ping sweep multi-threadé
- ✅ ARP scan
- ✅ Détection des ports ouverts
- ✅ Résolution hostname
- ✅ Export CSV & JSON
- ✅ Génération `.exe` via PyInstaller
- ✅ Multiplateforme (Windows/Linux/macOS)
- ✅ Extensible pour tests internes

---

## 🛠️ Prérequis

- Python 3.10+  
- Modules Python :

```bash
pip install -r requirements.txt


💻 Installation

Clonez le dépôt :

git clone https://github.com/TON_USERNAME/TON_REPO.git
cd TON_REPO

Installez les dépendances :

pip install -r requirements.txt

Lancez le scanner :

python main.py
📝 Utilisation
python main.py

Le script détecte automatiquement votre réseau local

Affiche la liste des machines actives et leurs ports ouverts

Génère scan_reseau.csv et scan_reseau.json

🖼️ Exemple de sortie
IP               HOSTNAME                   MAC               PORTS OUVERTS
10.0.81.1        Inconnu                   N/A               23,80,443
10.0.81.2        Inconnu                   N/A               22,23,80,443

Liens utiles

Python : https://www.python.org/

Scapy : https://scapy.net/

PyInstaller : https://www.pyinstaller.org/

Contributions

Contributions bienvenues !
Forkez, améliorez le scanner et proposez vos PR.

Auteur

Mouhamadou Mokhtar Thiam

Étudiant et passionné de cybersécurité et IoT
Email : mokhtar.thiam@securitenumerique-sn.com