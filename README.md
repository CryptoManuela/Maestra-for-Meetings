# Maestra for Meetings

Ein Tool zur automatischen Transkription und Zusammenfassung von Meeting-Aufnahmen.

## Features

- **Audio-Chunking**: Automatische Aufteilung großer Audio-Dateien (>50MB) für OpenAI Whisper
- **Transkription**: Hochwertige Transkription mit OpenAI Whisper
- **Zusammenfassung**: Intelligente Meeting-Zusammenfassungen mit Google Gemini

## Installation

```bash
# Repository klonen
git clone https://github.com/CryptoManuela/Maestra-for-Meetings.git
cd Maestra-for-Meetings

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# FFmpeg installieren (für Audio-Verarbeitung)
# Ubuntu/Debian: sudo apt install ffmpeg
# macOS: brew install ffmpeg
# Windows: https://ffmpeg.org/download.html
```

## Konfiguration

1. Kopiere `.env.example` zu `.env`:
   ```bash
   cp .env.example .env
   ```

2. Füge deine API-Keys in `.env` ein:
   - `OPENAI_API_KEY`: Dein OpenAI API Key für Whisper
   - `GOOGLE_API_KEY`: Dein Google Gemini API Key

## Verwendung

```bash
# Meeting transkribieren und zusammenfassen
python main.py meeting_aufnahme.mp3

# Nur transkribieren (ohne Zusammenfassung)
python main.py meeting_aufnahme.mp3 --no-summary

# Ausgabe in Datei speichern
python main.py meeting_aufnahme.mp3 -o output.txt

# Sprache explizit angeben
python main.py meeting_aufnahme.mp3 --language de
```

## Unterstützte Formate

- MP3, WAV, M4A, OGG, FLAC, WEBM, MP4

## Wie funktioniert das Audio-Chunking?

OpenAI Whisper hat ein Upload-Limit von 25MB pro Datei. Maestra teilt große Dateien automatisch in kleinere Chunks auf:

1. Audio wird in ~24MB Segmente aufgeteilt
2. Jedes Segment wird separat transkribiert
3. Die Transkriptionen werden intelligent zusammengeführt
4. Überlappungen werden erkannt und dedupliziert

## Lizenz

MIT License
