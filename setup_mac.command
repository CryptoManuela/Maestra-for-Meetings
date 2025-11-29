#!/bin/bash
# ============================================
# MAESTRA FOR MEETINGS - Automatisches Setup
# Doppelklick auf diese Datei zum Installieren
# ============================================

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║              MAESTRA FOR MEETINGS - SETUP                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Wechsle ins Skript-Verzeichnis
cd "$(dirname "$0")"

echo "📦 Installiere Abhängigkeiten..."
echo ""

# Prüfe ob Homebrew installiert ist
if ! command -v brew &> /dev/null; then
    echo "🍺 Installiere Homebrew (wird für FFmpeg benötigt)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Installiere FFmpeg
echo "🎬 Installiere FFmpeg..."
brew install ffmpeg 2>/dev/null || echo "FFmpeg bereits installiert"

# Erstelle virtuelle Umgebung
echo "🐍 Erstelle Python-Umgebung..."
python3 -m venv venv
source venv/bin/activate

# Installiere Python-Pakete
echo "📚 Installiere Python-Pakete..."
pip install --upgrade pip
pip install -r requirements.txt

# API Keys abfragen
echo ""
echo "============================================"
echo "🔑 API KEYS EINRICHTEN"
echo "============================================"
echo ""
echo "Du brauchst zwei API Keys:"
echo "1. OpenAI API Key (für Transkription)"
echo "2. Google API Key (für Zusammenfassung)"
echo ""

read -p "OpenAI API Key eingeben: " OPENAI_KEY
read -p "Google API Key eingeben: " GOOGLE_KEY

# .env Datei erstellen
cat > .env << EOF
# OpenAI API Key für Whisper Transkription
OPENAI_API_KEY=$OPENAI_KEY

# Google Gemini API Key für Meeting-Zusammenfassungen
GOOGLE_API_KEY=$GOOGLE_KEY

# Audio Chunk Einstellungen
MAX_CHUNK_SIZE_MB=24
CHUNK_OVERLAP_SECONDS=2
EOF

echo ""
echo "✅ API Keys gespeichert!"
echo ""
echo "✅ Installation abgeschlossen!"
echo ""
echo "============================================"
echo "SO VERWENDEST DU MAESTRA:"
echo "============================================"
echo ""
echo "Doppelklicke auf 'transkribieren.command'"
echo "und folge den Anweisungen."
echo ""

read -p "Drücke Enter zum Beenden..."
