"""
Motor de Groove Humano (human_groove_engine.py)
Añade swing, microtiming, velocity, ghost notes.
"""

import random

class HumanGrooveEngine:
    def __init__(self, varied_patterns):
        self.patterns = varied_patterns

    def add_human_groove(self):
        """Añade elementos humanos."""
        grooved_patterns = {}
        for section, pats in self.patterns.items():
            grooved_patterns[section] = self._apply_groove_to_section(pats)
        return grooved_patterns

    def _apply_groove_to_section(self, pats):
        """Aplica groove a una sección."""
        grooved = {}
        for instrument, events in pats.items():
            grooved[instrument] = []
            for ts, vel, idx in events:
                # Microtiming: desplazar en ms (±10ms)
                micro_shift = random.uniform(-0.01, 0.01)  # Segundos
                new_ts = ts + micro_shift
                # Swing en off-beats
                if ts % 1 == 0.5:  # Off-beat
                    new_ts += 0.02  # Swing
                # Variación velocity
                new_vel = vel * random.uniform(0.9, 1.1)
                # Ghost notes: añadir sutiles
                if random.random() < 0.1 and instrument == "perc":
                    grooved[instrument].append((new_ts + 0.1, new_vel * 0.3, idx))
                grooved[instrument].append((new_ts, new_vel, idx))
        return grooved