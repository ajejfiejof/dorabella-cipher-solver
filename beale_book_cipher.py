"""
Beale-Style Book Cipher Engine for Dorabella and Historical Cryptograms

Tests the hypothesis that Dorabella is a Book Cipher (like Beale Cipher #2),
utilizing a primary reference text to extract plaintext characters.
"""

import re
import string
from typing import List, Dict, Tuple, Optional
from dorabella_data import DorabellaSymbol, get_dorabella_symbol_sequence, SYMBOL_GRID_MAP


class BealeBookCipherEngine:

    def __init__(self, key_text: str):
        self.raw_text = key_text
        self.words = self._extract_words(key_text)
        self.lines = [line.strip() for line in key_text.strip().split("\n") if line.strip()]

    @staticmethod
    def _extract_words(text: str) -> List[str]:
        """Extract clean word tokens ignoring punctuation."""
        raw_tokens = text.split()
        words = []
        for t in raw_tokens:
            clean = t.strip(string.punctuation + string.whitespace)
            if clean:
                words.append(clean)
        return words

    def decode_beale_sequence(self, numbers: List[int]) -> str:
        """
        Classic Beale decoding:
        Each number N selects the 1st letter of the N-th word (1-indexed).
        """
        letters = []
        for num in numbers:
            idx = num - 1  # 1-indexed to 0-indexed
            if 0 <= idx < len(self.words):
                word = self.words[idx]
                first_letter = word[0].upper()
                letters.append(first_letter)
            else:
                letters.append("?")
        return "".join(letters)

    def decode_dorabella_direct_index(
        self,
        symbols: List[DorabellaSymbol],
        index_by: str = "symbol_value",  # "symbol_value", "direction", or "humps"
        letter_pos: int = 0
    ) -> str:
        """
        Mode A: Direct indexing.
        Each symbol maps to an index (1..24), extracting the letter_pos-th char of that word.
        """
        result = []
        for s in symbols:
            if index_by == "symbol_value":
                idx = (s.humps - 1) * 8 + s.direction
            elif index_by == "direction":
                idx = s.direction
            elif index_by == "humps":
                idx = s.humps - 1
            else:
                idx = 0

            if 0 <= idx < len(self.words):
                word = self.words[idx]
                char = word[letter_pos].upper() if len(word) > letter_pos else "?"
                result.append(char)
            else:
                result.append("?")
        return "".join(result)

    def decode_dorabella_word_gap_offset(
        self,
        symbols: List[DorabellaSymbol],
        wrap_around: bool = True
    ) -> str:
        """
        Mode B: Word-Gap Running Offset (Cumulative Beale Steganography).
        Each symbol specifies the gap distance (number of words to jump forward).
        """
        result = []
        current_word_idx = 0
        num_words = len(self.words)
        if num_words == 0:
            return ""

        for s in symbols:
            # Step size = value of symbol (1 to 24)
            step = (s.humps - 1) * 8 + s.direction + 1
            current_word_idx += step
            if wrap_around:
                current_word_idx %= num_words
            
            if current_word_idx < num_words:
                result.append(self.words[current_word_idx][0].upper())
            else:
                result.append("?")

        return "".join(result)

    def decode_dorabella_paired_beale(
        self,
        symbols: List[DorabellaSymbol],
        base: int = 8
    ) -> str:
        """
        Mode C: Paired Symbols as High-Range Beale Numbers.
        Since Dorabella has 87 characters, 43 pairs form 2-digit numbers:
        Pair (s1, s2) -> N = (s1_val * base) + s2_val + 1.
        Matches Beale number magnitudes (up to 576 or 64).
        """
        result = []
        for i in range(0, len(symbols) - 1, 2):
            s1 = symbols[i]
            s2 = symbols[i + 1]
            
            val1 = (s1.humps - 1) * 8 + s1.direction
            val2 = (s2.humps - 1) * 8 + s2.direction
            
            beale_num = (val1 * base) + val2 + 1
            idx = beale_num - 1
            if 0 <= idx < len(self.words):
                result.append(self.words[idx][0].upper())
            else:
                result.append("?")
        return "".join(result)
