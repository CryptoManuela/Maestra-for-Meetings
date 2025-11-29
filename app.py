#!/usr/bin/env python3
"""
Maestra for Meetings - Desktop App mit grafischer Oberfläche
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
from datetime import datetime

# Füge das aktuelle Verzeichnis zum Pfad hinzu
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from maestra.audio_chunker import get_audio_info
from maestra.transcriber import WhisperTranscriber
from maestra.summarizer import MeetingSummarizer


class MaestraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maestra for Meetings")
        self.root.geometry("700x600")
        self.root.configure(bg='#2b2b2b')

        self.selected_file = None
        self.result = {'transcript': None, 'summary': None}

        self.create_widgets()

    def create_widgets(self):
        # Titel
        title = tk.Label(
            self.root,
            text="🎙️ Maestra for Meetings",
            font=('Helvetica', 24, 'bold'),
            fg='white',
            bg='#2b2b2b'
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            self.root,
            text="Meeting-Transkription & Zusammenfassung",
            font=('Helvetica', 12),
            fg='#888888',
            bg='#2b2b2b'
        )
        subtitle.pack()

        # Datei-Auswahl Frame
        file_frame = tk.Frame(self.root, bg='#2b2b2b')
        file_frame.pack(pady=30, padx=40, fill='x')

        self.file_label = tk.Label(
            file_frame,
            text="Keine Datei ausgewählt",
            font=('Helvetica', 11),
            fg='#888888',
            bg='#3b3b3b',
            pady=20,
            padx=20
        )
        self.file_label.pack(fill='x')

        self.select_btn = tk.Button(
            file_frame,
            text="📁 Audio-Datei auswählen",
            font=('Helvetica', 14),
            bg='#4a9eff',
            fg='white',
            pady=10,
            cursor='hand2',
            command=self.select_file
        )
        self.select_btn.pack(fill='x', pady=(10, 0))

        # Sprache
        lang_frame = tk.Frame(self.root, bg='#2b2b2b')
        lang_frame.pack(pady=10)

        tk.Label(
            lang_frame,
            text="Sprache:",
            font=('Helvetica', 11),
            fg='white',
            bg='#2b2b2b'
        ).pack(side='left', padx=(0, 10))

        self.language = tk.StringVar(value='de')
        lang_menu = ttk.Combobox(
            lang_frame,
            textvariable=self.language,
            values=['de - Deutsch', 'en - English'],
            state='readonly',
            width=20
        )
        lang_menu.pack(side='left')

        # Start Button
        self.start_btn = tk.Button(
            self.root,
            text="🚀 Transkription starten",
            font=('Helvetica', 16, 'bold'),
            bg='#28a745',
            fg='white',
            pady=15,
            padx=40,
            cursor='hand2',
            command=self.start_processing,
            state='disabled'
        )
        self.start_btn.pack(pady=20)

        # Fortschritt
        self.progress_label = tk.Label(
            self.root,
            text="",
            font=('Helvetica', 11),
            fg='#888888',
            bg='#2b2b2b'
        )
        self.progress_label.pack()

        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=400
        )

        # Ergebnis
        result_frame = tk.Frame(self.root, bg='#2b2b2b')
        result_frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=('Helvetica', 10),
            bg='#1e1e1e',
            fg='white',
            height=10,
            wrap='word'
        )
        self.result_text.pack(fill='both', expand=True)

        # Speichern Button
        self.save_btn = tk.Button(
            self.root,
            text="💾 Ergebnis speichern",
            font=('Helvetica', 12),
            bg='#6c757d',
            fg='white',
            pady=8,
            cursor='hand2',
            command=self.save_result,
            state='disabled'
        )
        self.save_btn.pack(pady=(0, 20))

    def select_file(self):
        filetypes = [
            ('Audio-Dateien', '*.mp3 *.m4a *.wav *.ogg *.flac *.mp4 *.webm'),
            ('Alle Dateien', '*.*')
        ]

        filepath = filedialog.askopenfilename(
            title='Audio-Datei auswählen',
            filetypes=filetypes
        )

        if filepath:
            self.selected_file = filepath
            filename = os.path.basename(filepath)

            # Datei-Info holen
            try:
                info = get_audio_info(filepath)
                size = info.get('size_mb', 0)
                duration = info.get('duration_minutes', 0)

                self.file_label.config(
                    text=f"📄 {filename}\n{size:.1f} MB • {duration:.1f} Minuten",
                    fg='white'
                )
            except:
                self.file_label.config(text=f"📄 {filename}", fg='white')

            self.start_btn.config(state='normal')

    def start_processing(self):
        if not self.selected_file:
            return

        # UI aktualisieren
        self.start_btn.config(state='disabled')
        self.select_btn.config(state='disabled')
        self.progress.pack(pady=10)
        self.progress.start(10)
        self.progress_label.config(text="Transkription läuft... Bitte warten.")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "⏳ Verarbeitung gestartet...\n\n")

        # In separatem Thread ausführen
        thread = threading.Thread(target=self.process_audio)
        thread.start()

    def process_audio(self):
        try:
            lang = self.language.get().split(' - ')[0]

            # Transkription
            self.update_status("🎙️ Transkribiere Audio...")
            transcriber = WhisperTranscriber(language=lang)
            result = transcriber.transcribe(self.selected_file)
            self.result['transcript'] = result.text

            self.update_result(f"📝 TRANSKRIPTION:\n\n{result.text}\n\n")

            # Zusammenfassung
            self.update_status("📋 Erstelle Zusammenfassung...")
            summarizer = MeetingSummarizer(language=lang)
            summary = summarizer.summarize(result.text)
            self.result['summary'] = summary

            self.update_result(f"{'='*50}\n\n📋 ZUSAMMENFASSUNG:\n\n{summary}")

            self.update_status("✅ Fertig!")

        except Exception as e:
            self.update_status(f"❌ Fehler: {str(e)}")
            self.update_result(f"❌ Fehler aufgetreten:\n\n{str(e)}")

        finally:
            self.root.after(0, self.processing_done)

    def processing_done(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.start_btn.config(state='normal')
        self.select_btn.config(state='normal')
        self.save_btn.config(state='normal')

    def update_status(self, text):
        self.root.after(0, lambda: self.progress_label.config(text=text))

    def update_result(self, text):
        def update():
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, text)
        self.root.after(0, update)

    def save_result(self):
        if not self.result['transcript']:
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('Text-Datei', '*.txt'), ('Markdown', '*.md')],
            initialfile=f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Meeting Protokoll\n")
                f.write(f"Erstellt: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")

                if self.result['summary']:
                    f.write("## Zusammenfassung\n\n")
                    f.write(self.result['summary'])
                    f.write("\n\n---\n\n")

                f.write("## Transkription\n\n")
                f.write(self.result['transcript'])

            messagebox.showinfo("Gespeichert", f"Datei gespeichert:\n{filepath}")


def main():
    # Prüfe API Keys
    if not os.getenv('OPENAI_API_KEY'):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Fehler",
            "OpenAI API Key fehlt!\n\n"
            "Bitte führe zuerst setup_mac.command aus."
        )
        return

    root = tk.Tk()
    app = MaestraApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
