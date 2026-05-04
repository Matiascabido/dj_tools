"""
Motor de Evaluación Musical (music_evaluation_engine.py)
Responsabilidad: Evaluar calidad musical del track generado.
"""

import librosa
import numpy as np
from config.config import EVALUATION_THRESHOLDS, BPM

class MusicEvaluationEngine:
    def __init__(self):
        self.weights = {"groove": 0.3, "estructura": 0.2, "variacion": 0.2, "energia": 0.2, "dinamica": 0.1}

    def evaluate_track(self, track_path, structure):
        """Evalúa el track y retorna score y feedback."""
        try:
            y, sr = librosa.load(track_path, sr=None)
            scores = {}
            scores["groove"] = self._analyze_groove(y, sr)
            scores["estructura"] = self._analyze_structure(y, sr, structure)
            scores["variacion"] = self._analyze_variacion(y, sr, structure)
            scores["energia"] = self._analyze_energia(y)
            scores["dinamica"] = self._analyze_dinamica(y)

            total_score = sum(scores[k] * self.weights[k] for k in scores)
            feedback = {k: f"{v:.1f}/100" for k, v in scores.items()}
            return total_score, feedback
        except Exception as e:
            return 0, {"error": str(e)}

    def _analyze_groove(self, y, sr):
        """Analiza consistencia kick 4x4, síncopa."""
        # Detectar onsets
        onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
        # Estimar tempo
        tempo = librosa.feature.rhythm.tempo(y=y, sr=sr)[0]  # Nuevo en librosa 0.10
        # Simular kick cada beat (4x4)
        expected_kicks = len(onsets) / 4  # Aproximado
        score = min(100, (tempo / BPM) * 50 + (len(onsets) / expected_kicks) * 50)
        return score

    def _analyze_structure(self, y, sr, structure):
        """Verifica secciones y evolución."""
        duration = librosa.get_duration(y=y, sr=sr)
        expected_sections = len(structure["sections"])
        actual_sections = duration / 32  # Aproximado por sección
        score = min(100, (actual_sections / expected_sections) * 100)
        return score

    def _analyze_variacion(self, y, sr, structure):
        """Compara variación entre secciones."""
        # Dividir en secciones y comparar RMS
        section_durations = [sec["duration_beats"] * 60 / BPM for sec in structure["sections"].values()]
        rms_sections = []
        start = 0
        for dur in section_durations:
            end = start + dur
            if end > len(y) / sr:
                break
            rms = np.mean(librosa.feature.rms(y[int(start * sr):int(end * sr)]))
            rms_sections.append(rms)
            start = end
        # Variación: diferencia entre secciones
        if len(rms_sections) > 1:
            variation = np.std(rms_sections) / np.mean(rms_sections)
            score = min(100, variation * 1000)  # Más variación = mejor
        else:
            score = 50
        return score

    def _analyze_energia(self, y):
        """Estabilidad energética."""
        rms = librosa.feature.rms(y=y)
        stability = 1 - np.std(rms) / np.mean(rms)  # Menos varianza = más estable
        score = stability * 100
        return score

    def _analyze_dinamica(self, y):
        """Variación de volumen."""
        rms = librosa.feature.rms(y=y)
        dynamic_range = np.max(rms) - np.min(rms)
        score = min(100, dynamic_range * 1000)  # Más rango = mejor
        return score

    def improve_track(self, score, feedback, config_params):
        """Sugiere mejoras basadas en score."""
        improvements = []
        if score < 75:
            if feedback.get("groove", 0) < EVALUATION_THRESHOLDS["groove"]:
                improvements.append("Aumentar síncopa en percusión")
                config_params["ENERGY_LEVEL"] = min(10, config_params["ENERGY_LEVEL"] + 1)
            if feedback.get("variacion", 0) < EVALUATION_THRESHOLDS["variacion"]:
                improvements.append("Aumentar variación cada 8 compases")
            # Más ajustes...
        return improvements