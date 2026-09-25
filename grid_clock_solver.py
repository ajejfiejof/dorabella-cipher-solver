"""
Elgar's 3x8 Grid and Clock Rotation Cipher Solver
"""

import string
from typing import Dict, List, Tuple, Optional
from dorabella_data import DorabellaSymbol, get_dorabella_symbol_sequence, SYMBOL_GRID_MAP, DIRECTION_NAMES


def build_keyword_alphabet_24(keyword: str, omit_letters: Tuple[str, str] = ('J', 'V')) -> str:
    """
    Construct a 24-letter alphabet using a keyword, omitting two letters (traditionally J and V/Z).
    """
    clean_kw = "".join(ch.upper() for ch in keyword if ch.isalpha())
    seen = set(omit_letters)
    result = []
    
    for ch in clean_kw:
        if ch not in seen and ch in string.ascii_uppercase:
            seen.add(ch)
            result.append(ch)
            
    for ch in string.ascii_uppercase:
        if ch not in seen:
            seen.add(ch)
            result.append(ch)
            
    return "".join(result[:24])


class ElgarGridClockCipher:

    def __init__(
        self,
        grid_alphabet: Optional[str] = None,
        keyword: Optional[str] = None,
        omit_letters: Tuple[str, str] = ('J', 'V')
    ):
        if keyword:
            self.alphabet = build_keyword_alphabet_24(keyword, omit_letters)
        elif grid_alphabet and len(grid_alphabet) == 24:
            self.alphabet = grid_alphabet
        else:
            self.alphabet = build_keyword_alphabet_24("", omit_letters)

        # Build 3x8 grid (3 rows for humps 1..3, 8 columns for directions 0..7)
        self.grid: Dict[Tuple[int, int], str] = {}
        idx = 0
        for r in range(1, 4):      # humps 1, 2, 3
            for c in range(8):      # directions 0..7
                self.grid[(r, c)] = self.alphabet[idx]
                idx += 1

    def decode_symbols(self, symbols: List[DorabellaSymbol], clock_rotation: int = 0) -> str:
        """
        Decode symbols using the 3x8 grid, with an optional rotational offset on the clock direction.
        """
        decoded = []
        for s in symbols:
            # Rotate direction clockwise
            effective_dir = (s.direction + clock_rotation) % 8
            char = self.grid.get((s.humps, effective_dir), '?')
            decoded.append(char)
        return "".join(decoded)

    def print_grid(self):
        print("  Humps \\ Dir: " + "  ".join(DIRECTION_NAMES))
        print("  " + "-" * 42)
        for r in range(1, 4):
            row_chars = [self.grid[(r, c)] for c in range(8)]
            print(f"  Hump {r}     :  " + "   ".join(row_chars))
