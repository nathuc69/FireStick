# FireStick Remote

Télécommande virtuelle pour Amazon Fire TV Stick via ADB, avec une interface graphique Tkinter.

## Fonctionnalités

- **Scan réseau** : détecte automatiquement les Fire TV Stick sur le réseau local (port 5555)
- **Télécommande** : navigation directionnelle (haut, bas, gauche, droite, OK)
- **Navigation** : boutons Home, Back et Wake
- **Lancement d'apps** : Netflix, Prime Video, YouTube, Disney+
- **Saisie de texte** : envoyer du texte directement au Fire TV Stick

## Prérequis

- Python 3
- ADB installé et accessible dans le `PATH`
- Fire TV Stick avec le débogage ADB activé (Paramètres > Ma Fire TV > Options pour les développeurs > Débogage ADB)

## Installation

```bash
git clone https://github.com/nathuc69/FireStick.git
cd FireStick
python -m venv venv
source venv/bin/activate
pip install netifaces
```

## Utilisation

```bash
source venv/bin/activate
python remote.py
```

Ou directement :

```bash
./start.sh
```

1. Cliquer sur **Scan FireStick** pour détecter les appareils sur le réseau
2. Sélectionner un appareil dans la liste
3. Cliquer sur **Connect**
4. Utiliser les boutons de la télécommande

## Build (PyInstaller)

```bash
pip install pyinstaller
pyinstaller remote.spec
```

L'exécutable sera généré dans le dossier `dist/`.
