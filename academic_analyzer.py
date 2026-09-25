"""
Academic Decipherment Framework for the Dorabella Cipher
Based on methodologies from:
- Shannon (1949): Information Theory & Unicity Distance
- Kondrak, Hauer et al. (ACL/arXiv:2509.17950): Musical N-gram & Melodic Step Transition Analysis
- Lasry, Van Eycke & Oranchak (2020): Transposition-Substitution Decoupling (Zodiac Z340 methodology)
- Wase (Cryptologia, 2023): Hypothesis Testing against Monoalphabetic Models
"""

import math
import collections
from typing import List, Tuple, Dict
from dorabella_data import get_dorabella_symbol_sequence, DORABELLA_CIPHERTEXT, DorabellaSymbol


def calculate_shannon_entropy(data: List) -> float:
    """Calculate Shannon entropy H(X) in bits per symbol."""
    n = len(data)
    if n == 0:
        return 0.0
    counts = collections.Counter(data)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def calculate_conditional_entropy(data: List) -> float:
    """Calculate conditional bigram entropy H(X_i | X_{i-1})."""
    if len(data) < 2:
        return 0.0
    bigrams = [(data[i], data[i+1]) for i in range(len(data) - 1)]
    bg_counts = collections.Counter(bigrams)
    uni_counts = collections.Counter(data[:-1])
    
    total_bg = len(bigrams)
    cond_entropy = 0.0
    for (x_prev, x_curr), bg_c in bg_counts.items():
        p_xy = bg_c / total_bg
        p_y_given_x = bg_c / uni_counts[x_prev]
        cond_entropy -= p_xy * math.log2(p_y_given_x)
    return cond_entropy


def analyze_unicity_distance() -> Dict[str, float]:
    """
    Shannon Unicity Distance calculation:
    U = H(K) / D
    Where D = R_L * log2(|A|) - H_L (English redundancy ~ 3.2 bits/char)
    """
    d_english = 3.2  # redundancy bits/char
    
    # Model 1: MASC (24! keys)
    masc_key_bits = math.log2(math.factorial(24))
    u_masc = masc_key_bits / d_english
    
    # Model 2: Homophonic substitution (24 symbols for 15 most frequent English letters)
    homo_key_bits = math.log2(24**24)
    u_homo = homo_key_bits / d_english
    
    # Model 3: Transposition (87! permutations) + MASC
    trans_masc_bits = math.log2(math.factorial(87)) + masc_key_bits
    u_trans_masc = trans_masc_bits / d_english
    
    return {
        "U_MASC": u_masc,
        "U_Homophonic": u_homo,
        "U_Transposition_MASC": u_trans_masc,
        "Cipher_Length": 87.0
    }


def analyze_melodic_intervals(symbols: List[DorabellaSymbol]) -> Dict[str, float]:
    """
    Academic method from Hauer & Kondrak (arXiv:2509.17950):
    Test if symbol directions follow the 'stepwise motion' law of musical melodies.
    In natural melodies, ~70-80% of melodic transitions are conjunct (step sizes of 0, 1, or 2 semitones/scale degrees).
    """
    directions = [s.direction for s in symbols]
    intervals = []
    
    for i in range(len(directions) - 1):
        d1 = directions[i]
        d2 = directions[i + 1]
        # Circular difference on 8-point compass (modulo 8 distance)
        diff = abs(d2 - d1)
        circular_dist = min(diff, 8 - diff)
        intervals.append(circular_dist)
        
    counts = collections.Counter(intervals)
    total = len(intervals)
    
    # Step sizes:
    # 0 = repeated note (unison)
    # 1 = adjacent step (second)
    # 2 = skip (third)
    # 3 = leap (fourth)
    # 4 = tritone / octave midpoint leap
    stepwise_ratio = (counts.get(0, 0) + counts.get(1, 0) + counts.get(2, 0)) / total
    
    return {
        "step_0_unison": counts.get(0, 0) / total,
        "step_1_conjunct": counts.get(1, 0) / total,
        "step_2_skip": counts.get(2, 0) / total,
        "step_3_leap": counts.get(3, 0) / total,
        "step_4_wide": counts.get(4, 0) / total,
        "total_stepwise_ratio": stepwise_ratio
    }


def analyze_decoupled_streams(symbols: List[DorabellaSymbol]):
    """
    Decouple the 87 characters into:
    Stream A: Direction (8 states)
    Stream B: Humps (3 states)
    Calculate independent entropy and mutual information.
    """
    dirs = [s.direction for s in symbols]
    humps = [s.humps for s in symbols]
    
    h_dir = calculate_shannon_entropy(dirs)
    h_hump = calculate_shannon_entropy(humps)
    
    # Joint entropy
    joint = [(s.direction, s.humps) for s in symbols]
    h_joint = calculate_shannon_entropy(joint)
    
    # Mutual information I(Dir; Hump) = H(Dir) + H(Hump) - H(Joint)
    mutual_info = h_dir + h_hump - h_joint
    
    cond_h_dir = calculate_conditional_entropy(dirs)
    cond_h_hump = calculate_conditional_entropy(humps)
    
    return {
        "H_Direction": h_dir,
        "H_Humps": h_hump,
        "H_Joint": h_joint,
        "Mutual_Information": mutual_info,
        "Cond_H_Direction": cond_h_dir,
        "Cond_H_Humps": cond_h_hump
    }


def test_zodiac_style_transpositions(symbols: List[DorabellaSymbol]) -> List[Tuple[str, float, str]]:
    """
    Inspired by the 2020 solution of Zodiac Z340:
    Test structural transpositions:
    1. Standard reading (left to right, top to bottom)
    2. Columnar read (top to bottom, column by column)
    3. Alternating reverse (Boustrophedon)
    4. Diagonal / Knight's move (step 2 down 1 right, step 1 down 2 right)
    Returns entropy metrics for each candidate stream.
    """
    line1 = symbols[:29]
    line2 = symbols[29:60]
    line3 = symbols[60:87]
    
    candidates = {}
    
    # 1. Standard
    candidates["Standard (Row-Major)"] = [s.char_code for s in symbols]
    
    # 2. Boustrophedon (Line 2 reversed)
    candidates["Boustrophedon (L2 rev)"] = (
        [s.char_code for s in line1] +
        [s.char_code for s in reversed(line2)] +
        [s.char_code for s in line3]
    )
    
    # 3. Columnar (read down columns of 27 across the 3 lines)
    col_stream = []
    min_len = min(len(line1), len(line2), len(line3))
    for c in range(min_len):
        col_stream.append(line1[c].char_code)
        col_stream.append(line2[c].char_code)
        col_stream.append(line3[c].char_code)
    candidates["Columnar (Down 3 lines)"] = col_stream
    
    # 4. Diagonal Skip (1 down, 2 across)
    diag_stream = []
    grid = [line1, line2, line3]
    r, c = 0, 0
    visited = set()
    for _ in range(80):
        if c < len(grid[r]):
            key = (r, c)
            if key not in visited:
                visited.add(key)
                diag_stream.append(grid[r][c].char_code)
        r = (r + 1) % 3
        c = (c + 2) % 29
    candidates["Diagonal (1 down, 2 across)"] = diag_stream

    # Evaluate conditional bigram entropy for each transposition
    results = []
    for name, stream in candidates.items():
        cond_h = calculate_conditional_entropy(stream)
        results.append((name, cond_h, "".join(stream[:25])))
        
    results.sort(key=lambda x: x[1])
    return results
