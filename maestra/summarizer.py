"""
Summarizer - Google Gemini Integration für Meeting-Zusammenfassungen.

Erstellt intelligente Zusammenfassungen von Meeting-Transkriptionen
mit Aktionspunkten, Entscheidungen und wichtigen Themen.
"""

import os
from typing import Optional
import google.generativeai as genai


class MeetingSummarizer:
    """Erstellt Meeting-Zusammenfassungen mit Google Gemini."""

    DEFAULT_MODEL = "gemini-2.0-flash"

    # Standard-Prompt für Meeting-Zusammenfassungen (Deutsch)
    DEFAULT_PROMPT_DE = """Du bist ein Experte für Meeting-Zusammenfassungen.
Analysiere die folgende Meeting-Transkription und erstelle eine strukturierte Zusammenfassung.

Die Zusammenfassung soll enthalten:

## 📋 Überblick
Eine kurze Zusammenfassung des Meetings in 2-3 Sätzen.

## 👥 Teilnehmer
Liste der erkennbaren Teilnehmer (falls aus dem Kontext ersichtlich).

## 📌 Hauptthemen
Die wichtigsten besprochenen Themen als Aufzählung.

## ✅ Entscheidungen
Alle getroffenen Entscheidungen.

## 🎯 Aktionspunkte
Konkrete Aufgaben mit Verantwortlichen (falls genannt):
- [ ] Aufgabe 1 (@Person)
- [ ] Aufgabe 2 (@Person)

## 💡 Wichtige Erkenntnisse
Besonders wichtige Informationen oder Erkenntnisse.

## ❓ Offene Fragen
Fragen, die noch geklärt werden müssen.

---

MEETING-TRANSKRIPTION:

{transcript}

---

Erstelle nun die Zusammenfassung auf Deutsch:"""

    DEFAULT_PROMPT_EN = """You are an expert at meeting summarization.
Analyze the following meeting transcript and create a structured summary.

The summary should include:

## 📋 Overview
A brief summary of the meeting in 2-3 sentences.

## 👥 Participants
List of recognizable participants (if identifiable from context).

## 📌 Main Topics
The most important topics discussed as bullet points.

## ✅ Decisions
All decisions made during the meeting.

## 🎯 Action Items
Specific tasks with responsible persons (if mentioned):
- [ ] Task 1 (@Person)
- [ ] Task 2 (@Person)

## 💡 Key Insights
Particularly important information or insights.

## ❓ Open Questions
Questions that still need to be clarified.

---

MEETING TRANSCRIPT:

{transcript}

---

Now create the summary:"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        language: str = "de"
    ):
        """
        Initialisiert den Summarizer.

        Args:
            api_key: Google API Key (oder aus GOOGLE_API_KEY Umgebungsvariable)
            model: Gemini Modell
            language: Sprache für Zusammenfassung ('de' oder 'en')
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Google API Key nicht gefunden. "
                "Setze GOOGLE_API_KEY in .env oder übergebe api_key Parameter."
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)
        self.language = language

        # Wähle Prompt basierend auf Sprache
        self.prompt_template = (
            self.DEFAULT_PROMPT_DE if language == 'de'
            else self.DEFAULT_PROMPT_EN
        )

    def summarize(
        self,
        transcript: str,
        custom_prompt: Optional[str] = None
    ) -> str:
        """
        Erstellt eine Zusammenfassung der Meeting-Transkription.

        Args:
            transcript: Die Meeting-Transkription
            custom_prompt: Optionaler eigener Prompt (muss {transcript} enthalten)

        Returns:
            Die Zusammenfassung als String
        """
        prompt = custom_prompt or self.prompt_template

        if '{transcript}' not in prompt:
            raise ValueError("Prompt muss {transcript} Platzhalter enthalten.")

        full_prompt = prompt.format(transcript=transcript)

        print("Erstelle Meeting-Zusammenfassung mit Gemini...")

        response = self.model.generate_content(full_prompt)

        return response.text

    def summarize_with_focus(
        self,
        transcript: str,
        focus_areas: list[str]
    ) -> str:
        """
        Erstellt eine Zusammenfassung mit Fokus auf bestimmte Bereiche.

        Args:
            transcript: Die Meeting-Transkription
            focus_areas: Liste von Bereichen auf die fokussiert werden soll

        Returns:
            Die fokussierte Zusammenfassung
        """
        focus_str = "\n".join(f"- {area}" for area in focus_areas)

        custom_prompt = f"""Analysiere die folgende Meeting-Transkription und erstelle
eine Zusammenfassung mit besonderem Fokus auf diese Bereiche:

{focus_str}

MEETING-TRANSKRIPTION:

{{transcript}}

---

Erstelle eine detaillierte Zusammenfassung mit Fokus auf die genannten Bereiche:"""

        return self.summarize(transcript, custom_prompt)

    def extract_action_items(self, transcript: str) -> str:
        """
        Extrahiert nur die Aktionspunkte aus einer Transkription.

        Args:
            transcript: Die Meeting-Transkription

        Returns:
            Liste der Aktionspunkte
        """
        prompt = """Analysiere die folgende Meeting-Transkription und extrahiere
ALLE Aktionspunkte, Aufgaben und To-Dos.

Für jeden Aktionspunkt gib an:
- Die Aufgabe
- Wer verantwortlich ist (falls genannt)
- Deadline (falls genannt)
- Priorität (falls erkennbar)

Format:
- [ ] Aufgabe | Verantwortlich: @Person | Deadline: Datum | Priorität: Hoch/Mittel/Niedrig

MEETING-TRANSKRIPTION:

{transcript}

---

Extrahierte Aktionspunkte:"""

        return self.summarize(transcript, prompt)

    def generate_followup_email(self, transcript: str) -> str:
        """
        Generiert eine Follow-up E-Mail basierend auf der Transkription.

        Args:
            transcript: Die Meeting-Transkription

        Returns:
            E-Mail Text
        """
        prompt = """Basierend auf der folgenden Meeting-Transkription, erstelle eine
professionelle Follow-up E-Mail für alle Teilnehmer.

Die E-Mail soll enthalten:
- Betreff
- Freundliche Begrüßung
- Kurze Zusammenfassung der Besprechung
- Die wichtigsten Entscheidungen
- Aktionspunkte mit Verantwortlichen
- Nächste Schritte
- Freundlicher Abschluss

MEETING-TRANSKRIPTION:

{transcript}

---

Follow-up E-Mail:"""

        return self.summarize(transcript, prompt)
