#!/bin/bash
# ============================================
# MAESTRA FOR MEETINGS - App starten
# Doppelklick auf diese Datei
# ============================================

cd "$(dirname "$0")"

# Prüfe ob Setup schon lief
if [ ! -d "venv" ]; then
    osascript -e 'display alert "Setup erforderlich" message "Bitte führe zuerst setup_mac.command aus!" as critical'
    exit 1
fi

# Aktiviere Python-Umgebung und starte App
source venv/bin/activate
python app.py
