"""
Statistical and Monoalphabetic Substitution Cipher (MASC) Analyzer for Dorabella
"""

import collections
import math
import random
import string
from typing import Dict, List, Tuple
from dorabella_data import DORABELLA_CIPHERTEXT, DORABELLA_LINES


def calculate_ioc(text: str) -> float:
    """
    Calculate the Index of Coincidence (IoC).
    IoC = sum(f_i * (f_i - 1)) / (N * (N - 1))
    English ~ 0.0667, Random ~ 0.0385 (26 chars) or 0.0417 (24 chars).
    """
    n = len(text)
    if n <= 1:
        return 0.0
    counts = collections.Counter(text)
    numerator = sum(f * (f - 1) for f in counts.values())
    return numerator / (n * (n - 1))


def analyze_frequencies(text: str) -> List[Tuple[str, int, float]]:
    """Return sorted frequencies (char, count, percentage)."""
    counts = collections.Counter(text)
    total = len(text)
    return [(char, count, (count / total) * 100.0) for char, count in counts.most_common()]


def find_repeated_ngrams(text: str, n_range: range = range(2, 5)) -> Dict[int, List[Tuple[str, int, List[int]]]]:
    """Find repeated n-grams of specified lengths and their starting positions."""
    results = {}
    for n in n_range:
        seen = {}
        for i in range(len(text) - n + 1):
            gram = text[i : i + n]
            if gram not in seen:
                seen[gram] = []
            seen[gram].append(i)
        
        repeats = [(gram, len(pos_list), pos_list) for gram, pos_list in seen.items() if len(pos_list) > 1]
        repeats.sort(key=lambda x: x[1], reverse=True)
        results[n] = repeats
    return results


class SimpleHillClimbingMASC:
    """
    Hill-climbing solver using character and bigram statistics
    to demonstrate why standard MASC produces gibberish on Dorabella.
    """

    # Standard English character log-frequencies
    ENG_FREQ = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3,
        'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4,
        'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5, 'V': 1.0,
        'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
    }

    # Top English bigrams
    COMMON_BIGRAMS = {
        "TH": 3.8, "HE": 3.3, "IN": 2.4, "ER": 2.2, "AN": 2.1, "RE": 2.1,
        "ON": 2.0, "AT": 1.9, "EN": 1.8, "ND": 1.7, "TI": 1.6, "ES": 1.6,
        "OR": 1.5, "TE": 1.5, "OF": 1.4, "ED": 1.4, "IS": 1.3, "IT": 1.3,
        "AL": 1.3, "AR": 1.3, "ST": 1.3, "TO": 1.3, "NT": 1.2, "NG": 1.2,
        "SE": 1.2, "HA": 1.2, "AS": 1.2, "OU": 1.2, "IO": 1.2, "LE": 1.1,
        "VE": 1.1, "CO": 1.1, "ME": 1.1, "DE": 1.1, "HI": 1.1, "RI": 1.1,
        "RO": 1.1, "IC": 1.1, "NE": 1.1, "EA": 1.1, "RA": 1.1, "CE": 1.0
    }

    def __init__(self, ciphertext: str):
        self.ciphertext = ciphertext
        self.unique_symbols = sorted(list(set(ciphertext)))
        self.alphabet = list(string.ascii_uppercase)

    def score(self, text: str) -> float:
        """Score decrypted candidate using unigram and common bigram frequencies."""
        s = 0.0
        # Unigrams
        for ch in text:
            s += math.log(self.ENG_FREQ.get(ch, 0.01))
        # Bigrams
        for i in range(len(text) - 1):
            bg = text[i:i+2]
            if bg in self.COMMON_BIGRAMS:
                s += math.log(self.COMMON_BIGRAMS[bg] * 5.0)
            else:
                s += math.log(0.005)
        return s

    def solve(self, iterations: int = 3000, restarts: int = 5) -> Tuple[float, str, Dict[str, str]]:
        best_overall_score = -float('inf')
        best_overall_text = ""
        best_overall_key = {}

        for _ in range(restarts):
            # Random initial key mapping unique symbols to distinct uppercase letters
            shuffled_alpha = list(self.alphabet)
            random.shuffle(shuffled_alpha)
            current_key = {sym: shuffled_alpha[i] for i, sym in enumerate(self.unique_symbols)}
            
            def decrypt(key):
                return "".join(key.get(c, '?') for c in self.ciphertext)

            current_score = self.score(decrypt(current_key))

            for _ in range(iterations):
                # Pick two symbols to swap
                sym1, sym2 = random.sample(self.unique_symbols, 2)
                candidate_key = current_key.copy()
                candidate_key[sym1], candidate_key[sym2] = candidate_key[sym2], candidate_key[sym1]
                
                candidate_text = decrypt(candidate_key)
                candidate_score = self.score(candidate_text)

                if candidate_score > current_score:
                    current_score = candidate_score
                    current_key = candidate_key

            if current_score > best_overall_score:
                best_overall_score = current_score
                best_overall_key = current_key
                best_overall_text = decrypt(best_overall_key)

        return best_overall_score, best_overall_text, best_overall_key
