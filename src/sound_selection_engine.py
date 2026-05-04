"""
Motor de Selección de Sonidos (sound_selection_engine.py)
Responsabilidad: Elegir o generar sonidos adecuados para cada track, manteniendo coherencia.
"""

import os
import random
from pydub import AudioSegment
import numpy as np
from scipy.signal import sawtooth, square
from config.config import SOUND_MODE, ENERGY_LEVEL, SOUND_PALETTE, SYNTH_PARAMS

class SoundSelectionEngine:
    def __init__(self, track_type="hardgroove_main"):
        self.track_type = track_type
        self.energy_factor = ENERGY_LEVEL / 10.0  # Normalizar a 0-1

    def select_sounds(self):
        """
        Selecciona o genera sonidos basados en modo y energía.
        Retorna diccionario: {"kick": [AudioSegment o func], "hats": [...], ...}
        """
        sounds = {}
        for instrument in ["kick", "hats", "perc", "bass", "fx"]:
            if SOUND_MODE in ["base", "hybrid"]:
                # Seleccionar samples controladamente
                samples = self._select_samples(instrument)
                sounds[instrument] = samples if samples else self._generate_synth(instrument)
            elif SOUND_MODE == "advanced":
                sounds[instrument] = self._generate_synth(instrument)
        return sounds

    def _select_samples(self, instrument):
        """Selecciona samples de la paleta, con variación sutil basada en energía."""
        palette = SOUND_PALETTE.get(instrument, [])
        if not palette:
            return []
        # Seleccionar 1-3 samples, variando por energía (más variación en alta energía)
        num_select = min(len(palette), 1 + int(self.energy_factor * 2))
        selected = random.sample(palette, num_select)
        # Cargar como AudioSegment
        loaded = []
        for path in selected:
            if os.path.exists(path):
                loaded.append(AudioSegment.from_wav(path))
        return loaded

    def _generate_synth(self, instrument):
        """Genera sonido sintético con parámetros musicales."""
        params = SYNTH_PARAMS.get(instrument, {})
        freq = params.get("freq_base", 100) * (1 + self.energy_factor * 0.2)  # Variar frecuencia por energía
        duration = params.get("duration", 0.5)
        envelope = params.get("envelope", {"attack": 0.1, "decay": 0.2, "sustain": 0.5, "release": 0.2})

        # Generar onda (sinusoide para bass, sawtooth para fx, etc.)
        if instrument == "kick":
            wave = self._generate_kick_wave(freq, duration)
        elif instrument == "bass":
            wave = self._generate_bass_wave(freq, duration)
        else:
            wave = self._generate_fx_wave(freq, duration)

        # Aplicar envolvente ADSR
        wave = self._apply_envelope(wave, envelope, duration)

        # Retornar lista con función generadora para consistencia
        def generate_sound():
            return wave

        return [generate_sound]

    def _generate_kick_wave(self, freq, duration):
        """Genera onda para kick sintético."""
        t = np.linspace(0, duration, int(44100 * duration), False)
        # Onda exponencial decay para kick
        wave = np.exp(-t * 10) * np.sin(2 * np.pi * freq * t)
        return wave

    def _generate_bass_wave(self, freq, duration):
        """Genera onda para bass (sinusoide con variación)."""
        t = np.linspace(0, duration, int(44100 * duration), False)
        wave = np.sin(2 * np.pi * freq * t)
        return wave

    def _generate_fx_wave(self, freq, duration):
        """Genera onda para fx (sawtooth)."""
        t = np.linspace(0, duration, int(44100 * duration), False)
        wave = sawtooth(2 * np.pi * freq * t)
        return wave

    def _apply_envelope(self, wave, envelope, duration):
        """Aplica envolvente ADSR al wave, ajustando tiempos si exceden duration."""
        attack = envelope["attack"]
        decay = envelope["decay"]
        sustain = envelope["sustain"]
        release = envelope["release"]
        total_samples = len(wave)
        sample_rate = 44100

        # Ajustar tiempos si suman más que duration
        env_time = attack + decay + release
        if env_time > duration:
            factor = duration / env_time
            attack *= factor
            decay *= factor
            release *= factor

        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        release_samples = int(release * sample_rate)
        sustain_samples = max(0, total_samples - attack_samples - decay_samples - release_samples)

        # Construir envolvente
        env = np.concatenate([
            np.linspace(0, 1, attack_samples),  # Attack
            np.linspace(1, sustain, decay_samples),  # Decay
            np.full(sustain_samples, sustain),  # Sustain
            np.linspace(sustain, 0, release_samples)  # Release
        ])
        env = env[:total_samples]  # Ajustar longitud
        return wave * env