"""
Generador de Patrones Rítmicos (rhythm_pattern_generator.py)
Crea patrones rítmicos base para capas sonoras.
"""

import random
from config.config import SCALE

class RhythmPatternGenerator:
    def __init__(self, structure, sounds):
        self.structure = structure
        self.sounds = sounds
        self.scale_notes = self._get_scale_notes(SCALE)

    def generate_patterns(self):
        """
        Genera patrones por sección: listas de (timestamp, velocity, sound_index)
        """
        patterns = {}
        for section_name, section_data in self.structure["sections"].items():
            patterns[section_name] = self._generate_section_patterns(section_data)
        return patterns

    def _generate_section_patterns(self, section_data):
        """Genera patrones para una sección."""
        density = section_data["density"]
        duration_beats = section_data["duration_beats"]
        patterns = {"kick": [], "hats": [], "perc": [], "bass": [], "fx": []}

        # Kick: 4x4 constante
        for beat in range(int(duration_beats)):
            patterns["kick"].append((beat, 0.8, 0))  # Timestamp en beats, velocity, sound_index

        # Hats: ritmo constante con variación
        for beat in range(int(duration_beats)):
            for sub in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]:  # 16ths
                if random.random() < density:
                    patterns["hats"].append((beat + sub, 0.5, 0))

        # Perc: groove principal con síncopa
        for beat in range(int(duration_beats)):
            # Patrón base con variación
            base_pattern = [0, 1.5, 2, 3.5]  # Síncopa
            for offset in base_pattern:
                if random.random() < density:
                    patterns["perc"].append((beat + offset, 0.7, 0))

        # Bass: soporte rítmico/tonal
        for beat in range(0, int(duration_beats), 4):  # Cada 4 beats
            note = random.choice(self.scale_notes)
            patterns["bass"].append((beat, 0.6, note))  # Note como index o freq

        # FX: transiciones
        if density > 0.8:
            patterns["fx"].append((0, 0.4, 0))  # Al inicio de sección densa

        return patterns

    def _get_scale_notes(self, scale):
        """Retorna notas de la escala (simplificado)."""
        scales = {
            "D_minor": [50, 52, 55, 57, 59, 62, 64]  # Frecuencias base
        }
        return scales.get(scale, [50, 55, 60])