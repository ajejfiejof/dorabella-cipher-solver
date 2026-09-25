"""
Corpus of Edward Elgar's Melodic Themes (1888 - 1899)
For Melodic Alignment & Dynamic Time Warping against the Dorabella Cipher.
"""

from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ElgarTheme:
    title: str
    opus: str
    year: int
    key: str
    time_signature: str
    midi_pitches: List[int]
    parsons_code: str
    description: str


# Helper to compute Parsons code from pitches
def pitches_to_parsons(pitches: List[int]) -> str:
    if not pitches:
        return ""
    code = ["*"]
    for i in range(1, len(pitches)):
        if pitches[i] > pitches[i - 1]:
            code.append("u")
        elif pitches[i] < pitches[i - 1]:
            code.append("d")
        else:
            code.append("r")
    return "".join(code)


def _make_theme(title: str, opus: str, year: int, key: str, time_sig: str, pitches: List[int], desc: str) -> ElgarTheme:
    return ElgarTheme(
        title=title,
        opus=opus,
        year=year,
        key=key,
        time_signature=time_sig,
        midi_pitches=pitches,
        parsons_code=pitches_to_parsons(pitches),
        description=desc
    )


# 1. Variation X: "Dorabella" (Enigma Variations, Op. 36) - The flutter woodwind motif depicting Dora's stutter
# G Major, Allegretto: G4, B4, D5, E5, D5, B4, G4, A4, B4, G4, E4, D4...
THEME_DORABELLA = _make_theme(
    title="Enigma Variations: Var. X (Dorabella)",
    opus="Op. 36",
    year=1899,
    key="G Major",
    time_sig="3/4",
    pitches=[67, 71, 74, 76, 74, 71, 67, 69, 71, 67, 64, 62, 67, 71, 74, 76, 74, 71, 67, 69, 71],
    desc="Intermezzo dedicated to Dora Penny featuring graceful, fluttering woodwind trills."
)

# 2. Enigma Theme (Opening motif of Variations on an Original Theme, Op. 36)
# G Minor: Bb4, G4, C5, A4, Bb4, G4, D5...
THEME_ENIGMA = _make_theme(
    title="Enigma Theme (Original Theme)",
    opus="Op. 36",
    year=1899,
    key="G Minor",
    time_sig="4/4",
    pitches=[70, 67, 72, 69, 70, 67, 74, 72, 70, 69, 67, 65, 67, 69, 70],
    desc="The melancholic opening statement of the Enigma Variations."
)

# 3. Chanson de Matin (Op. 15 No. 2) - Composed Spring/Summer 1897!
# G Major: G4, B4, D5, G5, F#5, E5, D5, B4, C5, B4, A4...
THEME_CHANSON_DE_MATIN = _make_theme(
    title="Chanson de Matin",
    opus="Op. 15 No. 2",
    year=1897,
    key="G Major",
    time_sig="2/4",
    pitches=[67, 71, 74, 79, 78, 76, 74, 71, 72, 71, 69, 67, 71, 74, 79],
    desc="Composed in 1897 contemporaneous with the Dorabella letter; lyrical morning song."
)

# 4. Salut d'Amour (Op. 12) - Elgar's most famous romantic love token (1888)
# E Major / G Major: E5, D#5, E5, F#5, B4, G#5, F#5, E5...
THEME_SALUT_DAMOUR = _make_theme(
    title="Salut d'Amour (Liebesgruss)",
    opus="Op. 12",
    year=1888,
    key="E Major",
    time_sig="2/4",
    pitches=[76, 75, 76, 78, 71, 80, 78, 76, 74, 73, 74, 76, 69],
    desc="Love token given by Edward to Alice Roberts upon their engagement."
)

# 5. The Saga of King Olaf (Op. 30) - Composed 1896 (immediately prior to Dorabella visit)
# G Minor / D Minor: D4, G4, A4, Bb4, A4, G4, F#4, G4...
THEME_KING_OLAF = _make_theme(
    title="The Saga of King Olaf",
    opus="Op. 30",
    year=1896,
    key="G Minor",
    time_sig="4/4",
    pitches=[62, 67, 69, 70, 69, 67, 66, 67, 69, 70, 72, 74, 70],
    desc="Dramatic cantata composed by Elgar in 1896 for the North Staffordshire Festival."
)

# 6. The Black Knight (Op. 25) - Cantata (1893)
# D Minor: D4, F4, A4, D5, C#5, D5, Bb4, A4...
THEME_BLACK_KNIGHT = _make_theme(
    title="The Black Knight",
    opus="Op. 25",
    year=1893,
    key="D Minor",
    time_sig="4/4",
    pitches=[62, 65, 69, 74, 73, 74, 70, 69, 67, 65, 64, 62],
    desc="Choral symphony based on Uhland/Longfellow; established Elgar's choral reputation."
)

ELGAR_CORPUS: List[ElgarTheme] = [
    THEME_DORABELLA,
    THEME_ENIGMA,
    THEME_CHANSON_DE_MATIN,
    THEME_SALUT_DAMOUR,
    THEME_KING_OLAF,
    THEME_BLACK_KNIGHT,
]
