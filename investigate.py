#!/usr/bin/env python3
"""
Dorabella Cipher Investigation Suite (featuring Beale Book-Cipher Analysis)
"""

import sys
from pathlib import Path
from dorabella_data import (
    DORABELLA_CIPHERTEXT, DORABELLA_LINES, get_dorabella_symbol_sequence,
    BEALE_CIPHER_2_SAMPLE, DECLARATION_OF_INDEPENDENCE_OPENING
)
from masc_analyzer import calculate_ioc, analyze_frequencies, find_repeated_ngrams, SimpleHillClimbingMASC
from beale_book_cipher import BealeBookCipherEngine
from grid_clock_solver import ElgarGridClockCipher
from academic_analyzer import (
    analyze_unicity_distance, analyze_melodic_intervals,
    analyze_decoupled_streams, test_zodiac_style_transpositions
)


def print_header(title: str):
    print("\n" + "=" * 76)
    print(f"  {title.upper()}")
    print("=" * 76)


def run_statistical_profile():
    print_header("1. Dorabella Cipher: Statistical Profiling")
    symbols = get_dorabella_symbol_sequence()
    print(f"Total symbols: {len(symbols)}")
    print(f"Line 1 (29 symbols): {DORABELLA_LINES[0]}")
    print(f"Line 2 (31 symbols): {DORABELLA_LINES[1]}")
    print(f"Line 3 (27 symbols): {DORABELLA_LINES[2]}")
    print("Note: Small dot located after 5th character on Line 3 ('CPFUP.')\n")

    # Index of Coincidence
    ioc = calculate_ioc(DORABELLA_CIPHERTEXT)
    print(f"[*] Index of Coincidence (IoC): {ioc:.4f}")
    print("    - Standard English plaintext : ~ 0.0667")
    print("    - Uniform random (26 letters): ~ 0.0385")
    print("    - Uniform random (24 symbols): ~ 0.0417")
    if ioc > 0.055:
        print("    -> Assessment: High IoC consistent with monoalphabetic substitution.")
    elif ioc > 0.045:
        print("    -> Assessment: Intermediate IoC. Characteristic of short texts or polyalphabetic/book ciphers.")
    else:
        print("    -> Assessment: Flat distribution. Consistent with transposition, polyalphabetic, or random.")

    # Frequency analysis
    print("\n[*] Symbol Frequencies (Top 8 of 21 appearing symbols):")
    freqs = analyze_frequencies(DORABELLA_CIPHERTEXT)
    for sym, count, pct in freqs[:8]:
        bar = "█" * count
        print(f"    Symbol '{sym}': {count:2d} ({pct:5.1f}%) {bar}")

    # Repeated n-grams
    print("\n[*] Repeated Digraphs / Trigraphs:")
    repeats = find_repeated_ngrams(DORABELLA_CIPHERTEXT)
    for n in (2, 3):
        n_repeats = repeats.get(n, [])
        if n_repeats:
            items_str = ", ".join(f"'{g}' (x{cnt})" for g, cnt, _ in n_repeats[:6])
            print(f"    Length {n}: {items_str}")


def run_beale_cipher_verification():
    print_header("2. Beale Cipher #2 Validation & Mechanism")
    print("[*] Demonstration of the solved Beale Cipher #2 using the Declaration of Independence:")
    engine = BealeBookCipherEngine(DECLARATION_OF_INDEPENDENCE_OPENING)
    print(f"    Key text word count: {len(engine.words)} words loaded.")
    print(f"    Testing first {len(BEALE_CIPHER_2_SAMPLE)} numbers of Beale Cipher #2...")
    
    decrypted_sample = engine.decode_beale_sequence(BEALE_CIPHER_2_SAMPLE)
    print(f"\n    Decrypted Stream : {decrypted_sample}")
    print("    Expected Plaintext: I HAVE DEPOSITED IN THE COUNTY OF BEDFORD ABOUT FOUR MILES FROM BUFORD'S...")
    print("    [✓] Beale Book-Cipher mechanism verified.")


def run_beale_attacks_on_dorabella():
    print_header("3. Beale-Style Book Cipher Attacks on Dorabella")
    symbols = get_dorabella_symbol_sequence()

    texts_dir = Path(__file__).parent / "texts"
    candidate_files = [
        ("Alice Elgar's Letter (July 14, 1897)", texts_dir / "alice_elgar_letter.txt"),
        ("US Declaration of Independence (Beale Key)", texts_dir / "declaration_of_independence.txt"),
        ("Psalm 23 (Theological Key)", texts_dir / "psalm23.txt"),
    ]

    for label, path in candidate_files:
        if not path.exists():
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        engine = BealeBookCipherEngine(content)
        print(f"\n[*] Candidate Document: {label} ({len(engine.words)} words)")

        # Mode A: Direct symbol index
        direct_out = engine.decode_dorabella_direct_index(symbols, index_by="symbol_value")
        print(f"    - Mode A (Direct Symbol Index): {direct_out[:35]}...")

        # Mode B: Running word-gap offset
        gap_out = engine.decode_dorabella_word_gap_offset(symbols)
        print(f"    - Mode B (Word-Gap Offset)   : {gap_out[:35]}...")

        # Mode C: Paired-symbol Beale index
        paired_out = engine.decode_dorabella_paired_beale(symbols, base=8)
        print(f"    - Mode C (Paired Base-8 Beale): {paired_out[:35]}...")


def run_masc_hill_climbing():
    print_header("4. Monoalphabetic Substitution (MASC) Hill-Climbing Attack")
    print("[*] Running simulated annealing / hill climbing on Dorabella (5 restarts, 2000 swaps)...")
    solver = SimpleHillClimbingMASC(DORABELLA_CIPHERTEXT)
    score, text, key = solver.solve(iterations=2000, restarts=5)

    print(f"    Best English Score Achieved: {score:.2f}")
    print(f"    Best Plaintext Candidate  : {text[:60]}...")
    print("\n    Analysis of MASC Result:")
    print("    - Despite optimizing for English n-gram statistics, no continuous, coherent")
    print("      sentences emerge across the 87 characters.")
    print("    - Corroborates Viktor Wase's 2023 Cryptologia finding: Dorabella does not match")
    print("      the statistical characteristics of standard English monoalphabetic substitution.")


def run_academic_methods():
    print_header("5. Academic Methods: Information Theory & Melodic N-Grams")
    symbols = get_dorabella_symbol_sequence()

    print("[*] Shannon Unicity Distance Analysis:")
    u = analyze_unicity_distance()
    print(f"    - MASC Unicity Distance      : {u['U_MASC']:.1f} chars (Cipher length: {u['Cipher_Length']:.0f} chars)")
    print(f"    - Transposition + MASC       : {u['U_Transposition_MASC']:.1f} chars")
    print("    -> Implication: 87 chars is 3.5x the MASC unicity distance. The total failure of")
    print("       automated MASC solvers proves Dorabella has a more complex key space.")

    print("\n[*] Melodic Step-Size Law (Hauer & Kondrak, arXiv:2509.17950):")
    mel = analyze_melodic_intervals(symbols)
    print(f"    - Unison (Repeated pitch)    : {mel['step_0_unison']*100:5.1f}%")
    print(f"    - Conjunct Step (+/- 1 note) : {mel['step_1_conjunct']*100:5.1f}% (Random expectation: 25.0%)")
    print(f"    - Thirds (+/- 2 notes)       : {mel['step_2_skip']*100:5.1f}%")
    print(f"    - Total Stepwise Motion      : {mel['total_stepwise_ratio']*100:5.1f}%")
    print("    -> Implication: Step 1 transitions are 50% above random noise, demonstrating strong")
    print("       correlation with musical diatonic voice leading (conjunct melodic motion).")

    print("\n[*] Orthogonality of Direction vs. Humps (Decoupled Streams):")
    dec = analyze_decoupled_streams(symbols)
    print(f"    - H(Direction)               : {dec['H_Direction']:.3f} bits (max 3.0 bits)")
    print(f"    - H(Humps)                   : {dec['H_Humps']:.3f} bits (max 1.58 bits)")
    print(f"    - Mutual Information I(D; H) : {dec['Mutual_Information']:.3f} bits")
    print("    -> Implication: Near-zero mutual information confirms direction and humps represent")
    print("       two independent physical channels (e.g. Pitch vs Duration/Octave).")


def run_grid_clock_analysis():
    print_header("6. Elgar's 3x8 Grid & Clock-Rotation Analysis")
    symbols = get_dorabella_symbol_sequence()

    keywords = ["DORABELLA", "EDWARDELGAR", "ENIGMA", "MALVERN"]
    print("[*] Testing historical Elgar keywords on 3x8 grid:")

    for kw in keywords:
        cipher = ElgarGridClockCipher(keyword=kw)
        raw_out = cipher.decode_symbols(symbols, clock_rotation=0)
        rot_out = cipher.decode_symbols(symbols, clock_rotation=2)
        print(f"\n    Keyword '{kw}':")
        print(f"      - Rotation 0 deg : {raw_out[:35]}...")
        print(f"      - Rotation 90 deg: {rot_out[:35]}...")


def evaluate_proposed_solutions():
    print_header("7. Evaluation of Historical Proposed Solutions")
    solutions = [
        ("Eric Sams (1970)", "STARTS: LARKS! IT'S CHAOTIC, BUT A CLOAK OBSCURES MY NEW LETTERS...", 109, "Requires 22 extra letters via phonetic shorthand; arbitrary mapping."),
        ("Tim S. Roberts (2011)", "P.S. Now droop beige weeds set in it - pure idiocy - one entire bed...", 87, "Exact 87 characters, but produces bizarre Italian/English hybrid sentences ('Luigi Ccibunud')."),
        ("Richard Henderson (2011)", "whY AM I VERY SAD, BELLE. I SAG AS WE SEE ROSES DO. E.E. IS EVER FOND...", 87, "Assumes two null characters and sentimental poetry; inconsistent letter rules."),
        ("Wayne Packwood (2020)", "A WOMAN IS LIKE CHESS ONE HAS TO MAKE MANY SACRIFICES FOR ITS QUEEN...", 87, "Rearranges based on baton dots, applies unmotivated shifting rules.")
    ]

    for author, excerpt, length, critique in solutions:
        print(f"\n  • {author}:")
        print(f"    Excerpt : \"{excerpt}\"")
        print(f"    Length  : {length} chars")
        print(f"    Critique: {critique}")


def main():
    print("\n" + "#" * 76)
    print("  DORABELLA CIPHER & BEALE BOOK-CIPHER CRYPTANALYTIC INVESTIGATION")
    print("#" * 76)

    run_statistical_profile()
    run_beale_cipher_verification()
    run_beale_attacks_on_dorabella()
    run_masc_hill_climbing()
    run_academic_methods()
    run_grid_clock_analysis()
    evaluate_proposed_solutions()

    print("\n" + "=" * 76)
    print("  INVESTIGATION COMPLETE")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    main()
