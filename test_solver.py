import unittest
from dorabella_data import DORABELLA_CIPHERTEXT, get_dorabella_symbol_sequence, BEALE_CIPHER_2_SAMPLE, DECLARATION_OF_INDEPENDENCE_OPENING
from masc_analyzer import calculate_ioc, analyze_frequencies, find_repeated_ngrams
from beale_book_cipher import BealeBookCipherEngine
from grid_clock_solver import ElgarGridClockCipher, build_keyword_alphabet_24


class TestDorabellaSolver(unittest.TestCase):

    def test_cipher_length_and_symbols(self):
        symbols = get_dorabella_symbol_sequence()
        self.assertEqual(len(symbols), 87)
        self.assertEqual(len(DORABELLA_CIPHERTEXT), 87)
        # Check dot after char 5 on line 3
        dot_symbols = [s for s in symbols if s.has_dot_after]
        self.assertEqual(len(dot_symbols), 1)
        self.assertEqual(dot_symbols[0].line, 3)
        self.assertEqual(dot_symbols[0].col, 5)

    def test_ioc_calculation(self):
        ioc = calculate_ioc(DORABELLA_CIPHERTEXT)
        self.assertGreater(ioc, 0.050)
        self.assertLess(ioc, 0.065)

    def test_beale_cipher_decryption(self):
        sample_key_text = "In the heart and very center of our sacred land we find truth"
        engine = BealeBookCipherEngine(sample_key_text)
        # Word 1: In -> I
        # Word 3: heart -> H
        # Word 4: and -> A
        # Word 5: very -> V
        # Word 8: of -> O (or test IHAVE: 1, 3, 4, 5, ...)
        decoded = engine.decode_beale_sequence([1, 3, 4, 5])
        self.assertEqual(decoded, "IHAV")

    def test_elgar_grid_alphabet(self):
        alpha = build_keyword_alphabet_24("DORABELLA")
        self.assertEqual(len(alpha), 24)
        self.assertNotIn("J", alpha)
        self.assertNotIn("V", alpha)

        cipher = ElgarGridClockCipher(keyword="DORABELLA")
        symbols = get_dorabella_symbol_sequence()
        out = cipher.decode_symbols(symbols)
        self.assertEqual(len(out), 87)

    def test_music_engine_and_parsons(self):
        from music_engine import DorabellaMusicEngine
        symbols = get_dorabella_symbol_sequence()
        engine = DorabellaMusicEngine(scale_name="G_MAJOR", hump_mode="duration")
        melody = engine.symbols_to_melody(symbols)
        self.assertEqual(len(melody), 87)
        parsons = engine.calculate_parsons_code(melody)
        self.assertEqual(len(parsons), 87)
        self.assertEqual(parsons[0], "*")
        self.assertTrue(all(c in "*udr" for c in parsons))

    def test_melodic_matching(self):
        from music_engine import DorabellaMusicEngine
        from matcher import MelodicMatcher
        from elgar_themes import THEME_CHANSON_DE_MATIN
        symbols = get_dorabella_symbol_sequence()
        engine = DorabellaMusicEngine(scale_name="G_MAJOR", hump_mode="duration")
        melody = engine.symbols_to_melody(symbols)
        matcher = MelodicMatcher(melody)
        res = matcher.scan_theme(THEME_CHANSON_DE_MATIN)
        self.assertGreater(res.normalized_similarity, 0.70)
        self.assertGreater(res.z_score_vs_random, 2.0)

    def test_score_breaker_musical_syntax_and_cadence(self):
        from dorabella_score_breaker import DorabellaScoreBreaker
        breaker = DorabellaScoreBreaker(tempo_bpm=108)
        notes = breaker.decoded_notes

        self.assertEqual(len(notes), 87)

        # 1. Exposition Theme A: C5, B4, A4, G4 in 1-hump eighth notes
        theme_a_pitches = [n.note_name for n in notes[:4]]
        self.assertEqual(theme_a_pitches, ["C5", "B4", "A4", "G4"])
        self.assertTrue(all(n.humps == 1 for n in notes[:4]))

        # 2. Motivic Augmentation: C5, B4, A4, G4 in 2-hump quarter notes (indices 10..13)
        augmented_pitches = [n.note_name for n in notes[10:14]]
        self.assertEqual(augmented_pitches, ["C5", "B4", "A4", "G4"])
        self.assertTrue(all(n.humps == 2 for n in notes[10:14]))

        # 3. Dotted note: Line 3, Char 5 (index 64) is D5 with 1.5x duration
        dot_note = notes[64]
        self.assertTrue(dot_note.has_dot)
        self.assertEqual(dot_note.note_name, "D5")
        self.assertEqual(dot_note.duration_beats, 1.5)

        # 4. Melodic Climax: High G5 with 3 humps at index 63
        peak_note = notes[63]
        self.assertEqual(peak_note.note_name, "G5")
        self.assertEqual(peak_note.humps, 3)
        self.assertEqual(peak_note.duration_beats, 2.0)

        # 5. Final resolution to home Tonic G4 at index 86
        final_note = notes[86]
        self.assertEqual(final_note.note_name, "G4")

        # 6. ABC score format verification
        abc = breaker.generate_sheet_music_abc()
        self.assertIn("T: The Dorabella Cipher: Melodic Reconstruction", abc)
        self.assertIn("K: G", abc)
        self.assertTrue(abc.strip().endswith("|]"))


if __name__ == "__main__":
    unittest.main()

