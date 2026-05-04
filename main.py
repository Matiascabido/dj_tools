"""
Orquestador Principal (main.py)
Coordina todos los módulos para generar un track.
"""

import warnings
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg")

from src.web_sample_acquisition_engine import WebSampleAcquisitionEngine
from src.sound_selection_engine import SoundSelectionEngine
from src.structure_generator import StructureGenerator
from src.rhythm_pattern_generator import RhythmPatternGenerator
from src.variation_engine import VariationEngine
from src.human_groove_engine import HumanGrooveEngine
from src.harmonic_engine import HarmonicEngine
from src.mixing_engine import MixingEngine
from src.audio_renderer import AudioRenderer

def generate_track(track_name="track1"):
    # Adquirir samples web (opcional)
    acquisition_engine = WebSampleAcquisitionEngine()
    acquisition_engine.acquire_samples()

    # Seleccionar sonidos
    sound_engine = SoundSelectionEngine()
    sounds = sound_engine.select_sounds()

    # Generar estructura
    struct_gen = StructureGenerator(sounds)
    structure = struct_gen.generate_structure()

    # Generar patrones rítmicos
    rhythm_gen = RhythmPatternGenerator(structure, sounds)
    patterns = rhythm_gen.generate_patterns()

    # Aplicar variaciones
    var_engine = VariationEngine(patterns, structure["variation_markers"])
    varied_patterns = var_engine.apply_variations()

    # Añadir groove humano
    groove_engine = HumanGrooveEngine(varied_patterns)
    grooved_patterns = groove_engine.add_human_groove()

    # Integrar armonía
    harm_engine = HarmonicEngine(grooved_patterns)
    harmonic_patterns = harm_engine.integrate_harmony()

    # Mezclar
    mix_engine = MixingEngine(harmonic_patterns)
    mixed_patterns = mix_engine.mix_levels()

    # Renderizar
    renderer = AudioRenderer(mixed_patterns, sounds)
    output_path = f"output/{track_name}.wav"
    renderer.render_track(output_path)

    print(f"Track generado: {output_path}")

if __name__ == "__main__":
    generate_track()