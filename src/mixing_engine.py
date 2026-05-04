"""
Motor de Mezcla Básica (mixing_engine.py)
Mezcla niveles y evita conflictos.
"""

class MixingEngine:
    def __init__(self, harmonic_patterns):
        self.patterns = harmonic_patterns

    def mix_levels(self):
        """Ajusta niveles: kick dominante, bass controlado."""
        mixed_patterns = self.patterns.copy()
        for section, pats in mixed_patterns.items():
            for instrument, events in pats.items():
                for i, (ts, vel, idx) in enumerate(events):
                    if instrument == "kick":
                        new_vel = vel * 1.0  # Dominante
                    elif instrument == "bass":
                        new_vel = vel * 0.7  # Controlado
                    elif instrument in ["hats", "perc"]:
                        new_vel = vel * 0.5  # Suaves
                    else:
                        new_vel = vel * 0.4
                    pats[instrument][i] = (ts, new_vel, idx)
        return mixed_patterns