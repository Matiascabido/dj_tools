"""
Orquestador Principal (main.py)
Coordina todos los módulos para generar un track.
"""

import warnings
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg")

from src.sound_selection_engine import SoundSelectionEngine
from src.structure_generator import StructureGenerator
from src.rhythm_pattern_generator import RhythmPatternGenerator
from src.variation_engine import VariationEngine
from src.human_groove_engine import HumanGrooveEngine
from src.harmonic_engine import HarmonicEngine
from src.mixing_engine import MixingEngine
from src.audio_renderer import AudioRenderer
from src.music_evaluation_engine import MusicEvaluationEngine
from src.music_feedback_engine import MusicFeedbackEngine
from config.config import MAX_ITERATIONS

def generate_track(track_name="track1"):
    evaluator = MusicEvaluationEngine()
    feedback_engine = MusicFeedbackEngine()
    
    # Generar base una vez
    sound_engine = SoundSelectionEngine()
    sounds = sound_engine.select_sounds()
    struct_gen = StructureGenerator(sounds)
    structure = struct_gen.generate_structure()
    rhythm_gen = RhythmPatternGenerator(structure, sounds)
    patterns = rhythm_gen.generate_patterns()
    var_engine = VariationEngine(patterns, structure["variation_markers"])
    varied_patterns = var_engine.apply_variations()
    groove_engine = HumanGrooveEngine(varied_patterns)
    grooved_patterns = groove_engine.add_human_groove()
    harm_engine = HarmonicEngine(grooved_patterns)
    harmonic_patterns = harm_engine.integrate_harmony()
    mix_engine = MixingEngine(harmonic_patterns)
    mixed_patterns = mix_engine.mix_levels()

    for iteration in range(MAX_ITERATIONS):
        # Renderizar
        renderer = AudioRenderer(mixed_patterns, sounds)
        output_path = f"output/{track_name}.wav"
        renderer.render_track(output_path)

        # Evaluar
        score, feedback = evaluator.evaluate_track(output_path, structure)
        print(f"Iteración {iteration + 1}: Score {score:.1f}, Feedback: {feedback}")

        if score >= 75:
            print("Track válido generado.")
            break
        else:
            print("Aplicando correcciones...")
            actions = feedback_engine.analyze_and_correct(output_path, structure, mixed_patterns, evaluator)
            print(f"Acciones: {actions}")
            mixed_patterns = feedback_engine.apply_corrections(actions, mixed_patterns, structure)
            # Re-renderizar con correcciones aplicadas

    print(f"Track final: {output_path}")

if __name__ == "__main__":
    generate_track()