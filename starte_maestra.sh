#!/bin/bash

echo ""
echo "========================================"
echo "   MAESTRA FOR MEETINGS"
echo "   wird gestartet..."
echo "========================================"
echo ""

# Prüfe ob Python installiert ist
if ! command -v python3 &> /dev/null; then
    echo "FEHLER: Python3 ist nicht installiert!"
    echo "Bitte installiere Python von https://python.org"
    exit 1
fi

# Erstelle virtuelle Umgebung falls nicht vorhanden
if [ ! -d "venv" ]; then
    echo "Erstelle virtuelle Umgebung..."
    python3 -m venv venv
    echo ""
fi

# Aktiviere virtuelle Umgebung
source venv/bin/activate

# Installiere Abhängigkeiten
pip install -r requirements.txt --quiet

# Starte die App
echo ""
echo "App startet im Browser..."
echo "Drücke Strg+C zum Beenden"
echo ""
streamlit run app.py --server.headless true
