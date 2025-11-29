"""
Transcriber - OpenAI Whisper Integration für Transkription.

Transkribiert Audio-Dateien mit OpenAI's Whisper API und fügt
die Ergebnisse von gechunkten Dateien intelligent zusammen.
"""

import os
from pathlib import Path
from typing import List, Optional, Generator
from dataclasses import dataclass
from openai import OpenAI
from tqdm import tqdm

from .audio_chunker import AudioChunker


@dataclass
class TranscriptionSegment:
    """Ein Segment einer Transkription."""
    text: str
    chunk_index: int
    start_time: Optional[float] = None
    end_time: Optional[float] = None


@dataclass
class TranscriptionResult:
    """Ergebnis einer vollständigen Transkription."""
    text: str
    segments: List[TranscriptionSegment]
    language: Optional[str] = None
    duration_seconds: Optional[float] = None

    def __str__(self) -> str:
        return self.text


class WhisperTranscriber:
    """Transkribiert Audio mit OpenAI Whisper."""

    SUPPORTED_LANGUAGES = [
        'de', 'en', 'es', 'fr', 'it', 'pt', 'nl', 'pl', 'ru', 'ja', 'zh', 'ko'
    ]

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "whisper-1",
        language: Optional[str] = None,
        response_format: str = "text"
    ):
        """
        Initialisiert den Transcriber.

        Args:
            api_key: OpenAI API Key (oder aus OPENAI_API_KEY Umgebungsvariable)
            model: Whisper Modell (derzeit nur "whisper-1")
            language: Sprache des Audios (optional, wird sonst erkannt)
            response_format: Format der Antwort (text, json, srt, vtt)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API Key nicht gefunden. "
                "Setze OPENAI_API_KEY in .env oder übergebe api_key Parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.language = language
        self.response_format = response_format

    def transcribe_file(self, file_path: str) -> str:
        """
        Transkribiert eine einzelne Audio-Datei.

        Args:
            file_path: Pfad zur Audio-Datei

        Returns:
            Transkribierter Text
        """
        path = Path(file_path)

        with open(file_path, 'rb') as audio_file:
            kwargs = {
                'model': self.model,
                'file': audio_file,
                'response_format': self.response_format
            }

            if self.language:
                kwargs['language'] = self.language

            response = self.client.audio.transcriptions.create(**kwargs)

            # Je nach response_format ist die Antwort unterschiedlich
            if self.response_format == 'text':
                return response
            elif hasattr(response, 'text'):
                return response.text
            else:
                return str(response)

    def transcribe_chunks(
        self,
        chunk_paths: List[str],
        progress: bool = True
    ) -> TranscriptionResult:
        """
        Transkribiert mehrere Audio-Chunks und fügt sie zusammen.

        Args:
            chunk_paths: Liste von Pfaden zu Audio-Chunks
            progress: Zeige Fortschrittsbalken

        Returns:
            TranscriptionResult mit zusammengeführtem Text
        """
        segments = []

        iterator = enumerate(chunk_paths)
        if progress:
            iterator = tqdm(
                list(iterator),
                desc="Transkribiere",
                unit="chunk"
            )

        for i, chunk_path in iterator:
            text = self.transcribe_file(chunk_path)
            segment = TranscriptionSegment(
                text=text.strip(),
                chunk_index=i
            )
            segments.append(segment)

        # Füge Segmente zusammen und entferne Duplikate an Übergängen
        merged_text = self._merge_segments(segments)

        return TranscriptionResult(
            text=merged_text,
            segments=segments,
            language=self.language
        )

    def _merge_segments(self, segments: List[TranscriptionSegment]) -> str:
        """
        Fügt Transkriptions-Segmente intelligent zusammen.

        Erkennt und entfernt Duplikate an den Übergängen zwischen Chunks.
        """
        if not segments:
            return ""

        if len(segments) == 1:
            return segments[0].text

        merged_parts = []

        for i, segment in enumerate(segments):
            if i == 0:
                merged_parts.append(segment.text)
                continue

            current_text = segment.text

            # Versuche Überlappung zu finden
            previous_text = merged_parts[-1]
            overlap_removed = self._remove_overlap(previous_text, current_text)

            if overlap_removed:
                merged_parts.append(overlap_removed)
            else:
                # Keine Überlappung gefunden, füge mit Leerzeichen hinzu
                merged_parts.append(current_text)

        # Verbinde alle Teile
        return ' '.join(merged_parts)

    def _remove_overlap(
        self,
        previous: str,
        current: str,
        min_overlap_words: int = 3,
        max_overlap_words: int = 30
    ) -> Optional[str]:
        """
        Entfernt überlappenden Text am Anfang von 'current'.

        Args:
            previous: Vorheriger Text
            current: Aktueller Text
            min_overlap_words: Minimale Wörter für Überlappungserkennung
            max_overlap_words: Maximale Wörter zum Prüfen

        Returns:
            current ohne Überlappung, oder None wenn keine gefunden
        """
        prev_words = previous.split()
        curr_words = current.split()

        if len(prev_words) < min_overlap_words or len(curr_words) < min_overlap_words:
            return None

        # Suche nach Überlappung (letzte Wörter von previous = erste Wörter von current)
        for overlap_len in range(max_overlap_words, min_overlap_words - 1, -1):
            if overlap_len > len(prev_words) or overlap_len > len(curr_words):
                continue

            prev_end = prev_words[-overlap_len:]
            curr_start = curr_words[:overlap_len]

            # Vergleiche case-insensitive
            if [w.lower() for w in prev_end] == [w.lower() for w in curr_start]:
                # Überlappung gefunden - entferne vom current
                return ' '.join(curr_words[overlap_len:])

        return None

    def transcribe(
        self,
        file_path: str,
        max_chunk_size_mb: float = 24,
        progress: bool = True
    ) -> TranscriptionResult:
        """
        Transkribiert eine Audio-Datei (mit automatischem Chunking wenn nötig).

        Args:
            file_path: Pfad zur Audio-Datei
            max_chunk_size_mb: Maximale Größe pro Chunk
            progress: Zeige Fortschrittsbalken

        Returns:
            TranscriptionResult
        """
        chunker = AudioChunker(max_chunk_size_mb=max_chunk_size_mb)

        # Prüfe ob Chunking nötig ist
        if not chunker.needs_chunking(file_path):
            print("Datei ist klein genug für direkten Upload.")
            text = self.transcribe_file(file_path)
            return TranscriptionResult(
                text=text,
                segments=[TranscriptionSegment(text=text, chunk_index=0)],
                language=self.language
            )

        # Chunking erforderlich
        print(f"Datei zu groß ({chunker.get_file_size_mb(file_path):.1f} MB), starte Chunking...")

        with chunker:
            chunk_paths = list(chunker.chunk_audio(file_path, progress=progress))
            print(f"\nStarte Transkription von {len(chunk_paths)} Chunks...")
            result = self.transcribe_chunks(chunk_paths, progress=progress)

        return result
