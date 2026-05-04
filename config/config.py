import os

# Configuración global del sistema Hardgroove
# Parámetros musicales y de generación

# Modo de sonido: "base" (solo samples), "advanced" (solo síntesis), "hybrid" (combinado)
SOUND_MODE = "hybrid"

# Nivel de energía (1-10): afecta intensidad de sonidos y variaciones
ENERGY_LEVEL = 7

# BPM base (136-142 para Hardgroove)
BPM = 138

# Escala armónica (e.g., "D_minor")
SCALE = "D_minor"

# Duración mínima del track en minutos
MIN_DURATION_MIN = 5

# Ayuda a localizar WAVs dentro de las carpetas de samples
def get_sample_paths(relative_dir):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.normpath(os.path.join(base_dir, os.pardir, relative_dir))
    if not os.path.isdir(samples_dir):
        return []
    return sorted([
        os.path.join(relative_dir, f)
        for f in os.listdir(samples_dir)
        if f.lower().endswith(".wav")
    ])

# Paleta de sonidos base para coherencia entre tracks (rutas relativas o nombres)
SOUND_PALETTE = {
    "kick": get_sample_paths("samples/kick"),
    "hats": get_sample_paths("samples/hats"),
    "perc": get_sample_paths("samples/perc"),
    "bass": get_sample_paths("samples/bass"),
    "fx": get_sample_paths("samples/fx")
}

# Parámetros de síntesis
SYNTH_PARAMS = {
    "kick": {"freq_base": 60, "duration": 0.2, "envelope": {"attack": 0.005, "decay": 0.05, "sustain": 0.5, "release": 0.05}},
    "bass": {"freq_base": 50, "duration": 0.5, "envelope": {"attack": 0.02, "decay": 0.1, "sustain": 0.8, "release": 0.1}},
    "fx": {"freq_base": 200, "duration": 1.0, "envelope": {"attack": 0.05, "decay": 0.2, "sustain": 0.2, "release": 0.3}}
}

# Configuración de adquisición de samples locales y síntesis
SAMPLES_TO_DOWNLOAD = {
    "kick": 5,
    "hats": 10,
    "perc": 8,
    "bass": 3,
    "fx": 5
}

# Thresholds para análisis y clasificación
ANALYSIS_THRESHOLDS = {
    "kick": {"min_duration": 0.1, "max_duration": 0.5, "min_rms": 0.3},
    "hats": {"min_duration": 0.05, "max_duration": 0.3, "min_rms": 0.2},
    "perc": {"min_duration": 0.1, "max_duration": 1.0, "min_rms": 0.25},
    "bass": {"min_duration": 0.2, "max_duration": 2.0, "min_rms": 0.4},
    "fx": {"min_duration": 0.5, "max_duration": 5.0, "min_rms": 0.1}
}

# Configuración de evaluación musical
EVALUATION_THRESHOLDS = {
    "groove": 75,  # Consistencia kick, síncopa
    "estructura": 80,  # Secciones, evolución
    "variacion": 70,  # Cambios sutiles
    "energia": 75,  # Estabilidad RMS
    "dinamica": 70   # Variación volumen
}
MAX_ITERATIONS = 3  # Máximo iteraciones de mejora

# Reglas de feedback y correcciones
FEEDBACK_RULES = {
    "groove_bajo": ["aumentar_swing", "agregar_ghost_notes"],
    "robotico": ["variar_velocity", "introducir_microtiming"],
    "vacio": ["agregar_percusion"],
    "saturado": ["remover_elementos_secundarios"],
    "no_progresion": ["agregar_automatizacion"],
    "repeticion": ["regenerar_patron"]
}