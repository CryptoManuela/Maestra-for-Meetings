"""
Audio Chunker - Teilt große Audio-Dateien in kleinere Segmente auf.

OpenAI Whisper hat ein Upload-Limit von 25MB. Dieses Modul teilt große
Dateien automatisch in kleinere Chunks auf, die separat transkribiert
werden können.
"""

import os
import tempfile
import shutil
from pathlib import Path
from typing import List, Generator, Optional
from pydub import AudioSegment
from tqdm import tqdm


class AudioChunker:
    """Teilt Audio-Dateien in kleinere Segmente auf."""

    # OpenAI Whisper Limit ist 25MB, wir nutzen 24MB zur Sicherheit
    DEFAULT_MAX_SIZE_MB = 24
    DEFAULT_OVERLAP_SECONDS = 2

    # Unterstützte Formate
    SUPPORTED_FORMATS = {
        '.mp3': 'mp3',
        '.wav': 'wav',
        '.m4a': 'm4a',
        '.ogg': 'ogg',
        '.flac': 'flac',
        '.webm': 'webm',
        '.mp4': 'mp4',
    }

    def __init__(
        self,
        max_chunk_size_mb: float = DEFAULT_MAX_SIZE_MB,
        overlap_seconds: float = DEFAULT_OVERLAP_SECONDS,
        output_format: str = 'mp3',
        output_bitrate: str = '128k'
    ):
        """
        Initialisiert den AudioChunker.

        Args:
            max_chunk_size_mb: Maximale Größe pro Chunk in MB
            overlap_seconds: Überlappung zwischen Chunks in Sekunden
            output_format: Format der Output-Chunks (mp3 empfohlen für kleine Größe)
            output_bitrate: Bitrate für Output (niedrigere = kleinere Dateien)
        """
        self.max_chunk_size_bytes = int(max_chunk_size_mb * 1024 * 1024)
        self.overlap_ms = int(overlap_seconds * 1000)
        self.output_format = output_format
        self.output_bitrate = output_bitrate
        self.temp_dir: Optional[Path] = None

    def get_file_size_mb(self, file_path: str) -> float:
        """Gibt die Dateigröße in MB zurück."""
        return os.path.getsize(file_path) / (1024 * 1024)

    def needs_chunking(self, file_path: str) -> bool:
        """Prüft ob die Datei gechunkt werden muss."""
        return self.get_file_size_mb(file_path) > (self.max_chunk_size_bytes / (1024 * 1024))

    def load_audio(self, file_path: str) -> AudioSegment:
        """
        Lädt eine Audio-Datei.

        Args:
            file_path: Pfad zur Audio-Datei

        Returns:
            AudioSegment Objekt
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Nicht unterstütztes Format: {suffix}. "
                f"Unterstützt: {', '.join(self.SUPPORTED_FORMATS.keys())}"
            )

        format_name = self.SUPPORTED_FORMATS[suffix]

        print(f"Lade Audio-Datei: {path.name}")
        return AudioSegment.from_file(str(file_path), format=format_name)

    def estimate_chunk_duration(self, audio: AudioSegment) -> int:
        """
        Schätzt die optimale Chunk-Dauer basierend auf der Dateigröße.

        Args:
            audio: Das AudioSegment

        Returns:
            Geschätzte Dauer pro Chunk in Millisekunden
        """
        # Erstelle einen kurzen Test-Export um Bitrate zu messen
        test_duration_ms = min(10000, len(audio))  # 10 Sekunden oder weniger
        test_segment = audio[:test_duration_ms]

        with tempfile.NamedTemporaryFile(suffix=f'.{self.output_format}', delete=False) as f:
            test_path = f.name

        try:
            test_segment.export(
                test_path,
                format=self.output_format,
                bitrate=self.output_bitrate
            )
            test_size = os.path.getsize(test_path)

            # Berechne Bytes pro Millisekunde
            bytes_per_ms = test_size / test_duration_ms

            # Berechne wie viele Millisekunden in max_chunk_size passen
            chunk_duration_ms = int(self.max_chunk_size_bytes / bytes_per_ms)

            # Sicherheitsmarge von 10%
            chunk_duration_ms = int(chunk_duration_ms * 0.9)

            return chunk_duration_ms

        finally:
            if os.path.exists(test_path):
                os.remove(test_path)

    def chunk_audio(
        self,
        file_path: str,
        progress: bool = True
    ) -> Generator[str, None, None]:
        """
        Teilt eine Audio-Datei in Chunks auf.

        Args:
            file_path: Pfad zur Audio-Datei
            progress: Zeige Fortschrittsbalken

        Yields:
            Pfade zu den Chunk-Dateien
        """
        # Erstelle temporäres Verzeichnis für Chunks
        self.temp_dir = Path(tempfile.mkdtemp(prefix='maestra_chunks_'))

        # Wenn Datei klein genug ist, direkt zurückgeben
        if not self.needs_chunking(file_path):
            print(f"Datei ist klein genug ({self.get_file_size_mb(file_path):.1f} MB), kein Chunking nötig.")
            yield file_path
            return

        print(f"Datei ist {self.get_file_size_mb(file_path):.1f} MB, starte Chunking...")

        # Lade Audio
        audio = self.load_audio(file_path)
        total_duration_ms = len(audio)

        # Berechne optimale Chunk-Dauer
        chunk_duration_ms = self.estimate_chunk_duration(audio)

        print(f"Audio-Dauer: {total_duration_ms / 1000 / 60:.1f} Minuten")
        print(f"Chunk-Dauer: ~{chunk_duration_ms / 1000 / 60:.1f} Minuten pro Chunk")

        # Berechne Anzahl der Chunks
        num_chunks = (total_duration_ms // (chunk_duration_ms - self.overlap_ms)) + 1

        # Erstelle Chunks
        chunk_index = 0
        start_ms = 0

        iterator = range(num_chunks)
        if progress:
            iterator = tqdm(iterator, desc="Erstelle Chunks", unit="chunk")

        for _ in iterator:
            if start_ms >= total_duration_ms:
                break

            end_ms = min(start_ms + chunk_duration_ms, total_duration_ms)
            chunk = audio[start_ms:end_ms]

            # Speichere Chunk
            chunk_path = self.temp_dir / f"chunk_{chunk_index:04d}.{self.output_format}"
            chunk.export(
                str(chunk_path),
                format=self.output_format,
                bitrate=self.output_bitrate
            )

            yield str(chunk_path)

            # Nächster Chunk mit Überlappung
            start_ms = end_ms - self.overlap_ms
            chunk_index += 1

        print(f"Erstellt: {chunk_index} Chunks")

    def cleanup(self):
        """Löscht temporäre Chunk-Dateien."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()


def get_audio_info(file_path: str) -> dict:
    """
    Gibt Informationen über eine Audio-Datei zurück.

    Args:
        file_path: Pfad zur Audio-Datei

    Returns:
        Dict mit Datei-Informationen
    """
    path = Path(file_path)
    size_mb = os.path.getsize(file_path) / (1024 * 1024)

    info = {
        'path': str(path),
        'name': path.name,
        'format': path.suffix.lower(),
        'size_mb': round(size_mb, 2),
        'needs_chunking': size_mb > AudioChunker.DEFAULT_MAX_SIZE_MB
    }

    try:
        audio = AudioSegment.from_file(str(file_path))
        info['duration_seconds'] = len(audio) / 1000
        info['duration_minutes'] = round(len(audio) / 1000 / 60, 2)
        info['channels'] = audio.channels
        info['sample_rate'] = audio.frame_rate
    except Exception as e:
        info['error'] = str(e)

    return info
