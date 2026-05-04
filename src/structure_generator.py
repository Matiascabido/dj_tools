"""
Generador de Estructura (structure_generator.py)
Define la estructura temporal del track.
"""

from config.config import BPM, MIN_DURATION_MIN

class StructureGenerator:
    def __init__(self, sounds):
        self.sounds = sounds  # Diccionario de sonidos seleccionados
        self.bpm = BPM
        self.beats_per_measure = 4
        self.measures_per_phrase = 8  # Variación cada 8 compases
        self.min_duration_beats = MIN_DURATION_MIN * 60 * (BPM / 60)  # Convertir a beats

    def generate_structure(self):
        """
        Genera estructura: intro → main_a → drop → main_b → drop_b → main_a_2 → final
        Retorna diccionario con secciones y marcadores de variación.
        """
        sections = {
            "intro": {"start_beat": 0, "duration_beats": 32, "density": 0.3},
            "main_a": {"start_beat": 32, "duration_beats": 64, "density": 0.7},
            "drop": {"start_beat": 96, "duration_beats": 32, "density": 0.9},
            "main_b": {"start_beat": 128, "duration_beats": 64, "density": 0.8},
            "drop_b": {"start_beat": 192, "duration_beats": 32, "density": 0.95},
            "main_a_2": {"start_beat": 224, "duration_beats": 64, "density": 0.75},
            "final": {"start_beat": 288, "duration_beats": 32, "density": 0.4}
        }

        # Asegurar duración mínima
        total_beats = sum(sec["duration_beats"] for sec in sections.values())
        if total_beats < self.min_duration_beats:
            sections["final"]["duration_beats"] += self.min_duration_beats - total_beats

        # Marcadores de variación cada 8 compases
        variation_markers = []
        for beat in range(0, int(total_beats), self.measures_per_phrase * self.beats_per_measure):
            variation_markers.append(beat)

        return {"sections": sections, "variation_markers": variation_markers}