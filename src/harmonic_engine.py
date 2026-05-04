"""
Motor Armónico (harmonic_engine.py)
Gestiona escala y coherencia tonal.
"""

from config.config import SCALE

class HarmonicEngine:
    def __init__(self, grooved_patterns):
        self.patterns = grooved_patterns
        self.scale = SCALE

    def integrate_harmony(self):
        """Integra armonía, ajustando bass."""
        harmonic_patterns = self.patterns.copy()
        for section, pats in harmonic_patterns.items():
            # Ajustar bass para coherencia con escala
            for i, (ts, vel, note) in enumerate(pats["bass"]):
                # Mapear a escala
                harmonic_note = self._map_to_scale(note)
                pats["bass"][i] = (ts, vel, harmonic_note)
        return harmonic_patterns

    def _map_to_scale(self, note):
        """Mapea nota a escala (simplificado)."""
        scale_notes = {"D_minor": [50, 52, 55, 57, 59, 62, 64]}
        notes = scale_notes.get(self.scale, [50, 55, 60])
        return min(notes, key=lambda x: abs(x - note))