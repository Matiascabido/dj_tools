"""
Motor de Renderizado de Audio (audio_renderer.py)
Construye timeline y exporta WAV.
"""

from pydub import AudioSegment
import numpy as np
from config.config import BPM

class AudioRenderer:
    def __init__(self, mixed_patterns, sounds):
        self.patterns = mixed_patterns
        self.sounds = sounds
        self.sample_rate = 44100
        self.beat_duration = 60 / BPM  # Segundos por beat

    def render_track(self, output_path="output/track.wav"):
        """Renderiza y exporta WAV."""
        # Crear timeline vacío
        total_beats = max(ts for pats in self.patterns.values() for events in pats.values() for ts, _, _ in events)
        total_duration = total_beats * self.beat_duration
        timeline = AudioSegment.silent(duration=int(total_duration * 1000))

        for section, pats in self.patterns.items():
            for instrument, events in pats.items():
                sound_sources = self.sounds.get(instrument, [])
                if not sound_sources:
                    continue
                for ts, vel, idx in events:
                    start_ms = ts * self.beat_duration * 1000
                    if isinstance(sound_sources[0], AudioSegment):
                        # Sample
                        sound = sound_sources[min(idx, len(sound_sources)-1)].apply_gain(vel * 20 - 20)  # dB
                    else:
                        # Síntesis: llamar función
                        wave = sound_sources[0]()  # Función generadora
                        wave = (wave * vel * 32767).astype(np.int16)  # Normalizar
                        sound = AudioSegment(wave.tobytes(), frame_rate=self.sample_rate, sample_width=2, channels=1)
                    timeline = timeline.overlay(sound, position=int(start_ms))

        timeline.export(output_path, format="wav")
        return output_path