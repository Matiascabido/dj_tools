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

# Paleta de sonidos base para coherencia entre tracks (rutas relativas o nombres)
SOUND_PALETTE = {
    "kick": ["samples/kick/kick1.wav", "samples/kick/kick2.wav"],
    "hats": ["samples/hats/hat1.wav", "samples/hats/hat2.wav"],
    "perc": ["samples/perc/perc1.wav", "samples/perc/perc2.wav"],
    "bass": [],  # Vacío para síntesis
    "fx": []     # Vacío para síntesis
}

# Parámetros de síntesis
SYNTH_PARAMS = {
    "kick": {"freq_base": 60, "duration": 0.2, "envelope": {"attack": 0.005, "decay": 0.05, "sustain": 0.5, "release": 0.05}},
    "bass": {"freq_base": 50, "duration": 0.5, "envelope": {"attack": 0.02, "decay": 0.1, "sustain": 0.8, "release": 0.1}},
    "fx": {"freq_base": 200, "duration": 1.0, "envelope": {"attack": 0.05, "decay": 0.2, "sustain": 0.2, "release": 0.3}}
}

# Configuración de adquisición web de samples
ENABLE_WEB_ACQUISITION = True  # Ahora funciona sin API key
PIXABAY_API_KEY = ""  # No necesario, usa scraping
ENABLE_LANDR = True
ENABLE_LOOPMASTERS = False  # Requiere credenciales
LOOPMASTERS_USERNAME = ""
LOOPMASTERS_PASSWORD = ""

# Cantidad de samples a descargar por tipo
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