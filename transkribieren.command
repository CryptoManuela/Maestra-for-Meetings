#!/bin/bash
# ============================================
# MAESTRA FOR MEETINGS - Meeting transkribieren
# Doppelklick auf diese Datei zum Starten
# ============================================

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    MAESTRA FOR MEETINGS                       ║"
echo "║         Automatische Meeting-Transkription & Zusammenfassung  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Wechsle ins Skript-Verzeichnis
cd "$(dirname "$0")"

# Prüfe ob Setup schon lief
if [ ! -d "venv" ]; then
    echo "❌ Fehler: Setup wurde noch nicht ausgeführt!"
    echo ""
    echo "   Bitte führe zuerst setup_mac.command aus."
    echo ""
    read -p "Drücke Enter zum Beenden..."
    exit 1
fi

# Aktiviere virtuelle Umgebung
source venv/bin/activate

# Frage nach Audio-Datei
echo "🎵 Welche Audio-Datei möchtest du transkribieren?"
echo ""
echo "   TIPP: Ziehe die Datei einfach in dieses Fenster!"
echo ""
read -p "Dateipfad: " AUDIO_FILE

# Entferne eventuelle Anführungszeichen
AUDIO_FILE=$(echo "$AUDIO_FILE" | sed "s/^'//" | sed "s/'$//" | sed 's/\\ / /g')

if [ ! -f "$AUDIO_FILE" ]; then
    echo ""
    echo "❌ Fehler: Datei nicht gefunden!"
    echo "   Pfad: $AUDIO_FILE"
    echo ""
    read -p "Drücke Enter zum Beenden..."
    exit 1
fi

echo ""
echo "📁 Datei gefunden: $(basename "$AUDIO_FILE")"
echo ""

# Frage nach Sprache
echo "🌍 Welche Sprache wird im Meeting gesprochen?"
echo "   1) Deutsch"
echo "   2) Englisch"
echo "   3) Automatisch erkennen"
echo ""
read -p "Wähle (1/2/3): " LANG_CHOICE

case $LANG_CHOICE in
    1) LANGUAGE="--language de" ;;
    2) LANGUAGE="--language en" ;;
    *) LANGUAGE="" ;;
esac

echo ""
echo "🚀 Starte Verarbeitung..."
echo "   (Das kann bei langen Meetings einige Minuten dauern)"
echo ""

# Führe Maestra aus
python main.py "$AUDIO_FILE" $LANGUAGE

echo ""
echo "============================================"
echo "Die Ergebnisse findest du im Ordner 'output'"
echo "============================================"
echo ""

# Öffne Output-Ordner
open output 2>/dev/null

read -p "Drücke Enter zum Beenden..."
