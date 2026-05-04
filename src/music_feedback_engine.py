"""
Motor de Feedback y Corrección Musical (music_feedback_engine.py)
Responsabilidad: Detectar problemas y aplicar correcciones iterativas.
"""

import librosa
import numpy as np
from config.config import FEEDBACK_RULES, EVALUATION_THRESHOLDS

class MusicFeedbackEngine:
    def __init__(self):
        pass

    def analyze_and_correct(self, track_path, structure, patterns, evaluator):
        """Analiza problemas y retorna acciones correctivas."""
        problems = self._detect_problems(track_path, structure, patterns, evaluator)
        actions = []
        for prob in problems:
            actions.extend(FEEDBACK_RULES.get(prob, []))
        return list(set(actions))  # Unicos

    def _detect_problems(self, track_path, structure, patterns, evaluator):
        """Detecta problemas basados en métricas."""
        score, feedback = evaluator.evaluate_track(track_path, structure)
        problems = []
        if feedback.get("groove", 0) < EVALUATION_THRESHOLDS["groove"]:
            problems.append("groove_bajo")
        if self._is_robotico(track_path):
            problems.append("robotico")
        if self._is_vacio(patterns):
            problems.append("vacio")
        if self._is_saturado(patterns):
            problems.append("saturado")
        if feedback.get("energia", 0) < EVALUATION_THRESHOLDS["energia"]:
            problems.append("no_progresion")
        if self._has_repeticion(patterns):
            problems.append("repeticion")
        return problems

    def _is_robotico(self, track_path):
        """Detecta si suena robótico (poco swing/microtiming)."""
        y, sr = librosa.load(track_path, sr=None)
        # Simular: baja varianza en timing
        onsets = librosa.onset.onset_detect(y=y, sr=sr, units='samples')
        if len(onsets) > 1:
            intervals = np.diff(onsets)
            variance = np.var(intervals)
            return variance < 1000  # Threshold arbitrario
        return False

    def _is_vacio(self, patterns):
        """Detecta si falta densidad."""
        total_events = sum(len(events) for sec in patterns.values() for events in sec.values())
        return total_events < 100  # Threshold

    def _is_saturado(self, patterns):
        """Detecta saturación."""
        total_events = sum(len(events) for sec in patterns.values() for events in sec.values())
        return total_events > 500  # Threshold

    def _has_repeticion(self, patterns):
        """Detecta repetición de patrones."""
        # Comparar secciones
        sections = list(patterns.keys())
        if len(sections) > 1:
            sec1 = patterns[sections[0]]
            sec2 = patterns[sections[1]]
            # Simular comparación de eventos
            return len(sec1["kick"]) == len(sec2["kick"])  # Placeholder
        return False

    def apply_corrections(self, actions, patterns, structure):
        """Aplica correcciones a patrones/estructura."""
        if "aumentar_swing" in actions:
            # Aumentar swing en HumanGrooveEngine (simulado aquí)
            for sec in patterns.values():
                for events in sec.values():
                    for i, (ts, vel, idx) in enumerate(events):
                        if ts % 1 == 0.5:
                            events[i] = (ts + 0.03, vel, idx)  # Más swing
        if "agregar_ghost_notes" in actions:
            for sec in patterns.values():
                for i, (ts, vel, idx) in enumerate(sec["hats"]):
                    sec["hats"].append((ts + 0.1, vel * 0.3, idx))
        # Más acciones...
        return patterns