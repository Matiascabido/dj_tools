"""
Motor de Variación (variation_engine.py)
Aplica variaciones cada 8 compases.
"""

import random

class VariationEngine:
    def __init__(self, patterns, variation_markers):
        self.patterns = patterns
        self.variation_markers = variation_markers

    def apply_variations(self):
        """Aplica variaciones sutiles en marcadores."""
        varied_patterns = self.patterns.copy()
        for marker in self.variation_markers:
            for section, pats in varied_patterns.items():
                if section in ["main_a", "main_b", "main_a_2"]:  # Solo en secciones principales
                    self._vary_section(pats, marker)
        return varied_patterns

    def _vary_section(self, pats, marker):
        """Varía patrones en una sección."""
        # Añadir/quitar elementos sutilmente
        for instrument in ["perc", "hats"]:
            if random.random() < 0.3:  # 30% chance
                # Modificar velocity o añadir fill
                for i, (ts, vel, idx) in enumerate(pats[instrument]):
                    if ts >= marker and ts < marker + 8:
                        pats[instrument][i] = (ts, vel * random.uniform(0.8, 1.2), idx)