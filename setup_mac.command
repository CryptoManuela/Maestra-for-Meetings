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

# Erstelle .env falls nicht vorhanden
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  WICHTIG: API Keys werden benötigt!"
    echo ""
    cp .env.example .env
    echo "Bitte öffne die Datei .env und trage deine API Keys ein."
fi

echo ""
echo "✅ Installation abgeschlossen!"
echo ""
echo "============================================"
echo "SO VERWENDEST DU MAESTRA:"
echo "============================================"
echo ""
echo "1. Öffne Terminal"
echo "2. Ziehe 'transkribieren.command' ins Terminal"
echo "3. Ziehe deine Audio-Datei ins Terminal"
echo "4. Drücke Enter"
echo ""
echo "Oder doppelklicke auf 'transkribieren.command'"
echo "und folge den Anweisungen."
echo ""

read -p "Drücke Enter zum Beenden..."
