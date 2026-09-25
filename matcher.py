"""
Melodic Matching & Dynamic Time Warping (DTW) Engine
Compares Dorabella's pitch contour against Edward Elgar's historical themes.
"""

import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict
from elgar_themes import ElgarTheme, ELGAR_CORPUS, pitches_to_parsons
from music_engine import MusicalNote


@dataclass
class MatchResult:
    theme_title: str
    opus: str
    year: int
    best_window_idx: int
    matched_dorabella_subseq: str
    theme_parsons: str
    levenshtein_distance: int
    normalized_similarity: float
    dtw_distance: float
    z_score_vs_random: float


def levenshtein(s1: str, s2: str) -> int:
    """Standard Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def dtw_distance(seq1: List[float], seq2: List[float]) -> float:
    """Dynamic Time Warping distance between two 1D numerical sequences."""
    n, m = len(seq1), len(seq2)
    dtw_matrix = [[float('inf')] * (m + 1) for _ in range(n + 1)]
    dtw_matrix[0][0] = 0.0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(seq1[i - 1] - seq2[j - 1])
            dtw_matrix[i][j] = cost + min(
                dtw_matrix[i - 1][j],      # insertion
                dtw_matrix[i][j - 1],      # deletion
                dtw_matrix[i - 1][j - 1]   # match
            )

    return dtw_matrix[n][m] / max(n, m)


class MelodicMatcher:

    def __init__(self, dorabella_notes: List[MusicalNote]):
        self.notes = dorabella_notes
        self.pitches = [n.midi_pitch for n in dorabella_notes]
        self.parsons = pitches_to_parsons(self.pitches)

    def scan_theme(self, theme: ElgarTheme) -> MatchResult:
        """
        Slide the theme's Parsons contour along Dorabella's 87-note sequence
        to find the best local alignment window.
        """
        theme_p = theme.parsons_code[1:]  # strip leading '*'
        t_len = len(theme_p)
        d_p = self.parsons[1:]            # strip leading '*'

        best_dist = float('inf')
        best_idx = 0
        best_sub = ""

        # Slide window of size t_len across Dorabella contour
        for i in range(len(d_p) - t_len + 1):
            sub = d_p[i : i + t_len]
            dist = levenshtein(sub, theme_p)
            if dist < best_dist:
                best_dist = dist
                best_idx = i
                best_sub = sub

        similarity = 1.0 - (best_dist / max(t_len, 1))

        # DTW on relative pitch intervals
        # Normalize pitches by subtracting mean
        mean_d = sum(self.pitches[best_idx : best_idx + t_len]) / max(t_len, 1)
        norm_d = [p - mean_d for p in self.pitches[best_idx : best_idx + t_len]]
        
        mean_t = sum(theme.midi_pitches) / len(theme.midi_pitches)
        norm_t = [p - mean_t for p in theme.midi_pitches]
        
        dtw_val = dtw_distance(norm_d, norm_t)

        # Monte Carlo permutation test for statistical significance (Z-score)
        random_distances = []
        random_pool = list(d_p)
        for _ in range(200):
            random.shuffle(random_pool)
            rand_sub = "".join(random_pool[:t_len])
            random_distances.append(levenshtein(rand_sub, theme_p))

        mean_rnd = sum(random_distances) / len(random_distances)
        var_rnd = sum((x - mean_rnd) ** 2 for x in random_distances) / len(random_distances)
        std_rnd = math.sqrt(var_rnd) if var_rnd > 0 else 1.0
        z_score = (mean_rnd - best_dist) / std_rnd

        return MatchResult(
            theme_title=theme.title,
            opus=theme.opus,
            year=theme.year,
            best_window_idx=best_idx,
            matched_dorabella_subseq=best_sub,
            theme_parsons=theme_p,
            levenshtein_distance=best_dist,
            normalized_similarity=similarity,
            dtw_distance=dtw_val,
            z_score_vs_random=z_score
        )

    def scan_all_themes(self, corpus: List[ElgarTheme] = ELGAR_CORPUS) -> List[MatchResult]:
        results = [self.scan_theme(t) for t in corpus]
        # Sort by similarity descending
        results.sort(key=lambda x: (x.normalized_similarity, x.z_score_vs_random), reverse=True)
        return results
