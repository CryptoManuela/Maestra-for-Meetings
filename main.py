#!/usr/bin/env python3
"""
Maestra for Meetings - Hauptanwendung

Automatische Transkription und Zusammenfassung von Meeting-Aufnahmen.
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

# Lade .env Datei
load_dotenv()

from maestra.audio_chunker import AudioChunker, get_audio_info
from maestra.transcriber import WhisperTranscriber
from maestra.summarizer import MeetingSummarizer


def print_header():
    """Druckt den Anwendungs-Header."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                    MAESTRA FOR MEETINGS                       ║
║         Automatische Meeting-Transkription & Zusammenfassung  ║
╚═══════════════════════════════════════════════════════════════╝
""")


def print_audio_info(file_path: str):
    """Zeigt Informationen über die Audio-Datei."""
    info = get_audio_info(file_path)

    print("\n📁 Audio-Datei Info:")
    print(f"   Name: {info['name']}")
    print(f"   Format: {info['format']}")
    print(f"   Größe: {info['size_mb']:.2f} MB")

    if 'duration_minutes' in info:
        print(f"   Dauer: {info['duration_minutes']:.1f} Minuten")

    if info['needs_chunking']:
        print(f"   ⚠️  Datei benötigt Chunking (>24 MB)")
    else:
        print(f"   ✅ Datei kann direkt verarbeitet werden")

    print()


def process_meeting(
    audio_path: str,
    output_path: str = None,
    language: str = None,
    skip_summary: bool = False,
    summary_only: bool = False,
    transcript_path: str = None,
    model: str = "gpt-4o-transcribe",
    prompt: str = None
) -> dict:
    """
    Verarbeitet eine Meeting-Aufnahme.

    Args:
        audio_path: Pfad zur Audio-Datei
        output_path: Optionaler Pfad für Output-Datei
        language: Sprache des Audios
        skip_summary: Überspringe Zusammenfassung
        summary_only: Nur Zusammenfassung (erfordert transcript_path)
        transcript_path: Pfad zu existierender Transkription
        model: OpenAI Transkriptions-Modell
        prompt: Basis-Prompt für Kontext (Fachbegriffe, Namen etc.)

    Returns:
        Dict mit transcript und summary
    """
    result = {
        'transcript': None,
        'summary': None
    }

    # Wenn nur Zusammenfassung gewünscht
    if summary_only and transcript_path:
        print("📄 Lade existierende Transkription...")
        with open(transcript_path, 'r', encoding='utf-8') as f:
            result['transcript'] = f.read()
    else:
        # Transkription erstellen
        print("\n🎙️  SCHRITT 1: Transkription mit OpenAI")
        print("=" * 50)

        transcriber = WhisperTranscriber(
            language=language,
            model=model,
            base_prompt=prompt
        )
        transcription_result = transcriber.transcribe(audio_path)
        result['transcript'] = transcription_result.text

        print("\n✅ Transkription abgeschlossen!")
        print(f"   Textlänge: {len(result['transcript'])} Zeichen")
        print(f"   Wörter: {len(result['transcript'].split())} Wörter")

    # Zusammenfassung erstellen
    if not skip_summary:
        print("\n\n📝 SCHRITT 2: Zusammenfassung mit Google Gemini")
        print("=" * 50)

        summarizer = MeetingSummarizer(language=language or 'de')
        result['summary'] = summarizer.summarize(result['transcript'])

        print("\n✅ Zusammenfassung abgeschlossen!")

    # Output speichern
    if output_path:
        save_results(result, output_path)
    else:
        # In Standard-Output-Verzeichnis speichern
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = Path(audio_path).stem if audio_path else 'meeting'

        # Transkription speichern
        transcript_file = output_dir / f"{base_name}_{timestamp}_transcript.txt"
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(result['transcript'])
        print(f"\n📄 Transkription gespeichert: {transcript_file}")

        # Zusammenfassung speichern
        if result['summary']:
            summary_file = output_dir / f"{base_name}_{timestamp}_summary.md"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(result['summary'])
            print(f"📋 Zusammenfassung gespeichert: {summary_file}")

    return result


def save_results(result: dict, output_path: str):
    """Speichert die Ergebnisse in einer Datei."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Meeting Protokoll\n\n")
        f.write(f"Erstellt: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")

        if result['summary']:
            f.write("---\n\n")
            f.write(result['summary'])
            f.write("\n\n")

        f.write("---\n\n")
        f.write("## Vollständige Transkription\n\n")
        f.write(result['transcript'])

    print(f"\n✅ Ergebnisse gespeichert: {output_path}")


def main():
    """Hauptfunktion."""
    parser = argparse.ArgumentParser(
        description='Maestra for Meetings - Meeting-Transkription und Zusammenfassung',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  python main.py meeting.mp3                    # Transkription + Zusammenfassung
  python main.py meeting.mp3 --no-summary       # Nur Transkription
  python main.py meeting.mp3 -o protokoll.md    # Mit Output-Datei
  python main.py meeting.mp3 --language de      # Sprache angeben
  python main.py --info meeting.mp3             # Nur Datei-Info anzeigen

  # Mit Kontext-Prompt für bessere Erkennung:
  python main.py meeting.mp3 --prompt "Meeting über KI-Projekt mit Max, Lisa und Dr. Schmidt"

  # Mit anderem Modell:
  python main.py meeting.mp3 --model gpt-4o-mini-transcribe   # Schneller/günstiger
        """
    )

    parser.add_argument(
        'audio_file',
        nargs='?',
        help='Pfad zur Audio-Datei (MP3, WAV, M4A, etc.)'
    )

    parser.add_argument(
        '-o', '--output',
        help='Pfad für die Ausgabe-Datei'
    )

    parser.add_argument(
        '-l', '--language',
        choices=['de', 'en', 'es', 'fr', 'it', 'pt', 'nl'],
        help='Sprache des Audios (wird sonst automatisch erkannt)'
    )

    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Überspringe die Zusammenfassung'
    )

    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Nur Zusammenfassung erstellen (benötigt --transcript)'
    )

    parser.add_argument(
        '--transcript',
        help='Pfad zu existierender Transkription (für --summary-only)'
    )

    parser.add_argument(
        '--info',
        action='store_true',
        help='Zeige nur Informationen über die Audio-Datei'
    )

    parser.add_argument(
        '--action-items',
        action='store_true',
        help='Extrahiere nur Aktionspunkte aus Transkription'
    )

    parser.add_argument(
        '--email',
        action='store_true',
        help='Generiere Follow-up E-Mail aus Transkription'
    )

    parser.add_argument(
        '-m', '--model',
        choices=['gpt-4o-transcribe', 'gpt-4o-mini-transcribe', 'whisper-1'],
        default='gpt-4o-transcribe',
        help='OpenAI Transkriptions-Modell (Standard: gpt-4o-transcribe)'
    )

    parser.add_argument(
        '-p', '--prompt',
        help='Kontext-Prompt für bessere Erkennung (z.B. Teilnehmernamen, Fachbegriffe)'
    )

    args = parser.parse_args()

    # Wenn keine Audio-Datei angegeben
    if not args.audio_file and not args.summary_only:
        parser.print_help()
        sys.exit(1)

    print_header()

    # Prüfe ob Datei existiert
    if args.audio_file and not os.path.exists(args.audio_file):
        print(f"❌ Fehler: Datei nicht gefunden: {args.audio_file}")
        sys.exit(1)

    # Nur Info anzeigen
    if args.info:
        print_audio_info(args.audio_file)
        sys.exit(0)

    # Prüfe API Keys
    if not os.getenv('OPENAI_API_KEY') and not args.summary_only:
        print("❌ Fehler: OPENAI_API_KEY nicht gesetzt!")
        print("   Erstelle eine .env Datei mit deinem API Key.")
        sys.exit(1)

    if not os.getenv('GOOGLE_API_KEY') and not args.no_summary:
        print("❌ Fehler: GOOGLE_API_KEY nicht gesetzt!")
        print("   Erstelle eine .env Datei mit deinem API Key.")
        sys.exit(1)

    # Audio-Info anzeigen
    if args.audio_file:
        print_audio_info(args.audio_file)

    # Summary-only Modus
    if args.summary_only:
        if not args.transcript:
            print("❌ Fehler: --summary-only benötigt --transcript")
            sys.exit(1)

        result = process_meeting(
            audio_path=None,
            output_path=args.output,
            language=args.language,
            summary_only=True,
            transcript_path=args.transcript,
            model=args.model,
            prompt=args.prompt
        )
    else:
        # Normale Verarbeitung
        result = process_meeting(
            audio_path=args.audio_file,
            output_path=args.output,
            language=args.language,
            skip_summary=args.no_summary,
            model=args.model,
            prompt=args.prompt
        )

    # Spezielle Ausgaben
    if args.action_items and result['transcript']:
        print("\n\n🎯 AKTIONSPUNKTE")
        print("=" * 50)
        summarizer = MeetingSummarizer(language=args.language or 'de')
        action_items = summarizer.extract_action_items(result['transcript'])
        print(action_items)

    if args.email and result['transcript']:
        print("\n\n📧 FOLLOW-UP E-MAIL")
        print("=" * 50)
        summarizer = MeetingSummarizer(language=args.language or 'de')
        email = summarizer.generate_followup_email(result['transcript'])
        print(email)

    print("\n\n✨ Verarbeitung abgeschlossen!")


if __name__ == '__main__':
    main()
