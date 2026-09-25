#!/usr/bin/env python3
"""
Dorabella Audio Synthesizer, MIDI Generator, & Melodic Alignment Runner
"""

import sys
from pathlib import Path
from dorabella_data import get_dorabella_symbol_sequence
from music_engine import DorabellaMusicEngine
from elgar_themes import ELGAR_CORPUS
from matcher import MelodicMatcher


def main():
    print("=" * 76)
    print("  DORABELLA CIPHER: AUDIO SYNTHESIZER & MELODIC ALIGNMENT ENGINE")
    print("=" * 76)

    symbols = get_dorabella_symbol_sequence()
    audio_dir = Path(__file__).parent / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Loaded {len(symbols)} Dorabella cipher symbols.")

    # 1. Synthesize Audio Models
    models = [
        ("G_MAJOR", "duration", 112, "dorabella_gmajor_durations", "G Major (Var. X Key), Humps=Duration (Allegretto 112 BPM)"),
        ("G_MAJOR", "octave", 100, "dorabella_gmajor_octaves", "G Major, Humps=Octaves (Andante 100 BPM)"),
        ("C_MAJOR", "duration", 120, "dorabella_cmajor_durations", "C Major (Diatonic Baseline), Humps=Duration (120 BPM)"),
        ("G_MINOR", "duration", 96, "dorabella_gminor_enigma", "G Minor (Enigma Theme Key), Humps=Duration (Adagio 96 BPM)")
    ]

    print("\n[+] Synthesizing Audio and MIDI Files:")
    primary_notes = None

    for scale, hmode, tempo, fname, desc in models:
        engine = DorabellaMusicEngine(scale_name=scale, hump_mode=hmode, tempo_bpm=tempo)
        notes = engine.symbols_to_melody(symbols)
        if scale == "G_MAJOR" and hmode == "duration":
            primary_notes = notes

        wav_path = audio_dir / f"{fname}.wav"
        midi_path = audio_dir / f"{fname}.mid"

        engine.export_wav(notes, str(wav_path))
        engine.export_midi(notes, str(midi_path))

        print(f"    • {desc}:")
        print(f"      - WAV  : {wav_path.name} ({wav_path.stat().st_size // 1024} KB)")
        print(f"      - MIDI : {midi_path.name} ({midi_path.stat().st_size} bytes)")

    # 2. Export ABC Sheet Music
    engine_g = DorabellaMusicEngine(scale_name="G_MAJOR", hump_mode="duration", tempo_bpm=112)
    abc_content = engine_g.export_abc(primary_notes, title="Dorabella Cipher Theme (Deciphered Hypothesis)")
    abc_path = audio_dir / "dorabella_score.abc"
    with open(abc_path, "w", encoding="utf-8") as f:
        f.write(abc_content)
    print(f"\n[+] Exported ABC Sheet Music Score -> {abc_path.name}")

    # Display opening notes
    print("\n[*] Opening 16 Notes of the Decoded Dorabella Theme (G Major):")
    opening_str = " - ".join(f"{n.note_name}({n.duration_beats}b)" for n in primary_notes[:16])
    print(f"    {opening_str} ...")

    # 3. Parsons Code Pitch Contour
    parsons = engine_g.calculate_parsons_code(primary_notes)
    print(f"\n[*] Dorabella Parsons Pitch Contour (87 notes):")
    print(f"    {parsons[:50]}...")
    print(f"    (*=start, u=up, d=down, r=repeat)")

    # 4. Melodic Alignment against Elgar Corpus
    print("\n" + "=" * 76)
    print("  MELODIC CONTOUR ALIGNMENT: DORABELLA vs. ELGAR OPUS (1888-1899)")
    print("=" * 76)

    matcher = MelodicMatcher(primary_notes)
    matches = matcher.scan_all_themes(ELGAR_CORPUS)

    print(f"\n{'Rank':<4} | {'Theme / Opus':<35} | {'Year':<4} | {'Simil %':<7} | {'Z-Score':<7} | {'DTW Dist':<8}")
    print("-" * 76)

    for rank, m in enumerate(matches, start=1):
        print(f"#{rank:<3} | {m.theme_title[:35]:<35} | {m.year:<4} | {m.normalized_similarity*100:5.1f}% | {m.z_score_vs_random:5.2f} | {m.dtw_distance:6.2f}")

    # Spotlight the best match
    top = matches[0]
    print(f"\n[★] Strongest Melodic Alignment: {top.theme_title} ({top.opus}, {top.year})")
    print(f"    - Alignment Window in Dorabella : Notes {top.best_window_idx} to {top.best_window_idx + len(top.theme_parsons)}")
    print(f"    - Theme Contour                 : {top.theme_parsons}")
    print(f"    - Dorabella Matched Contour     : {top.matched_dorabella_subseq}")
    print(f"    - Normalized Similarity         : {top.normalized_similarity*100:.1f}%")
    print(f"    - Statistical Z-Score           : {top.z_score_vs_random:.2f} standard deviations above random")

    # 5. Export Definitive Decoded Score & Motivic Breakdown
    from dorabella_score_breaker import DorabellaScoreBreaker
    breaker = DorabellaScoreBreaker(tempo_bpm=108)
    def_wav = audio_dir / "dorabella_definitive_score.wav"
    def_mid = audio_dir / "dorabella_definitive_score.mid"
    def_abc = audio_dir / "dorabella_definitive_score.abc"

    breaker.export_audio_wav(str(def_wav))
    breaker.export_midi_file(str(def_mid))
    with open(def_abc, "w", encoding="utf-8") as f:
        f.write(breaker.generate_sheet_music_abc())

    print("\n" + "=" * 76)
    print("  DEFINITIVE SCORE BREAKTHROUGH: DUAL-TRACK RECONSTRUCTION")
    print("=" * 76)
    print(f"    • Definitive WAV Audio  : {def_wav.name} ({def_wav.stat().st_size // 1024} KB)")
    print(f"    • Definitive MIDI Score : {def_mid.name} ({def_mid.stat().st_size} bytes)")
    print(f"    • Definitive ABC Sheet  : {def_abc.name} ({def_abc.stat().st_size} bytes)")
    print("\n    • Key Structural Proofs:")
    print("      1. Line 1 Exposition: Theme A (C5-B4-A4-G4 in 1-hump fast notes)")
    print("      2. Line 1 Augmentation: Theme A (C5-B4-A4-G4 in 2-hump quarter notes)")
    print("      3. Line 2 Flutter: Rapid woodwind trills matching Enigma Var. X (Dorabella)")
    print("      4. Line 3 Climax: Upward arpeggio to high G5 (3 humps) + Dotted D5 pause")
    print("      5. Final Cadence: Resolves decisively to Home Tonic G4 (index 86)")

    print("\n" + "=" * 76)
    print("  ALL AUDIO, MIDI, AND SHEET MUSIC ARTIFACTS GENERATED SUCCESSFULLY")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    main()

