"""
Dorabella Cipher and Beale Cipher Reference Data & Transcriptions
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass
class DorabellaSymbol:
    char_code: str
    line: int
    col: int
    humps: int         # 1, 2, or 3 semicircles
    direction: int     # 0 to 7 (compass points: 0=E, 1=SE, 2=S, 3=SW, 4=W, 5=NW, 6=N, 7=NE)
    direction_name: str
    has_dot_after: bool = False


# Standard letter-based transcription of the 87 Dorabella symbols (MysteryTwister / ACA standard)
# Line 1: 29 chars
# Line 2: 31 chars
# Line 3: 27 chars (Dot occurs after char 5: 'C P F U P .')
DORABELLA_LINES = [
    "ABCDEFGDHAIJKLJMJJFBBJNGOGNIP",
    "GJGFQDHRSCJJCFNKGJIJFTPKLQHHQIP",
    "CPFUPCLUUNPCJFUKPNDBNPFDLED"
]

DORABELLA_CIPHERTEXT = "".join(DORABELLA_LINES)

# 8 compass directions mapped to 45-degree angles
DIRECTION_NAMES = ["E", "SE", "S", "SW", "W", "NW", "N", "NE"]

# Approximate visual symbol mapping to (humps, direction) based on Elgar's 3x8 alphabet:
# In the standard transcription, symbols A through U are mapped:
SYMBOL_GRID_MAP: Dict[str, Tuple[int, int]] = {
    'A': (1, 0), 'B': (1, 1), 'C': (1, 2), 'D': (1, 3),
    'E': (1, 4), 'F': (1, 5), 'G': (1, 6), 'H': (1, 7),
    'I': (2, 0), 'J': (2, 1), 'K': (2, 2), 'L': (2, 3),
    'M': (2, 4), 'N': (2, 5), 'O': (2, 6), 'P': (2, 7),
    'Q': (3, 0), 'R': (3, 1), 'S': (3, 2), 'T': (3, 3),
    'U': (3, 4), 'V': (3, 5), 'W': (3, 6), 'X': (3, 7),
}


def get_dorabella_symbol_sequence() -> List[DorabellaSymbol]:
    """Return all 87 Dorabella symbols with line, position, humps, and direction."""
    sequence: List[DorabellaSymbol] = []
    for line_idx, line_str in enumerate(DORABELLA_LINES, start=1):
        for col_idx, char in enumerate(line_str, start=1):
            humps, direction = SYMBOL_GRID_MAP.get(char, (1, 0))
            is_dot = (line_idx == 3 and col_idx == 5)
            sequence.append(DorabellaSymbol(
                char_code=char,
                line=line_idx,
                col=col_idx,
                humps=humps,
                direction=direction,
                direction_name=DIRECTION_NAMES[direction],
                has_dot_after=is_dot
            ))
    return sequence


# BEALE CIPHER #2: The Solved Beale Cipher (762 numbers) - First 60 numbers sample for validation
BEALE_CIPHER_2_SAMPLE = [
    115, 73, 24, 807, 37, 52, 49, 17, 31, 62, 647, 22, 7, 15, 140, 47, 29, 107, 79, 84, 56, 239, 10,
    26, 811, 5, 196, 308, 85, 52, 160, 136, 59, 211, 36, 9, 110, 4, 91, 459, 300, 84, 279, 74, 59,
    10, 12, 654, 413, 108, 17, 471, 33, 10, 36, 85, 18, 508, 58, 27
]

# The opening of the US Declaration of Independence (Key text for Beale Cipher #2)
DECLARATION_OF_INDEPENDENCE_OPENING = """
When in the Course of human events it becomes necessary for one people to dissolve the
political bands which have connected them with another and to assume among the powers
of the earth the separate and equal station to which the Laws of Nature and of Nature's
God entitle them a decent respect to the opinions of mankind requires that they should
declare the causes which impel them to the separation. We hold these truths to be
self-evident, that all men are created equal, that they are endowed by their Creator
with certain unalienable Rights, that among these are Life, Liberty and the pursuit of
Happiness. That to secure these rights, Governments are instituted among Men, deriving
their just powers from the consent of the governed, That whenever any Form of Government
becomes destructive of these ends, it is the Right of the People to alter or to abolish it,
and to institute new Government, laying its foundation on such principles and organizing
its powers in such form, as to them shall seem most likely to effect their Safety and
Happiness. Prudence, indeed, will dictate that Governments long established should not be
changed for light and transient causes; and accordingly all experience hath shewn that
mankind are more disposed to suffer, while evils are sufferable than to right themselves
by abolishing the forms to which they are accustomed. But when a long train of abuses and
usurpations, pursuing invariably the same Object evinces a design to reduce them under
absolute Despotism, it is their right, it is their duty, to throw off such Government,
and to provide new Guards for their future security. Such has been the patient sufferance
of these Colonies; and such is now the necessity which constrains them to alter their
former Systems of Government. The history of the present King of Great Britain is a
history of repeated injuries and usurpations, all having in direct object the establishment
of an absolute Tyranny over these States. To prove this, let Facts be submitted to a candid
world. He has refused his Assent to Laws, the most wholesome and necessary for the public
good. He has forbidden his Governors to pass Laws of immediate and pressing importance,
unless suspended in their operation till his Assent should be obtained; and when so
suspended, he has utterly neglected to attend to them. He has refused to pass other Laws
for the accommodation of large districts of people, unless those people would relinquish
the right of Representation in the Legislature, a right inestimable to them and formidable
to tyrants only. He has called together legislative bodies at places unusual, uncomfortable,
and distant from the depository of their public Records, for the sole purpose of fatiguing
them into compliance with his measures. He has dissolved Representative Houses repeatedly,
for opposing with manly firmness his invasions on the rights of the people. He has refused
for a long time, after such dissolutions, to cause others to be elected; whereby the
Legislative powers, incapable of Annihilation, have returned to the People at large for
their exercise; the State remaining in the mean time exposed to all the dangers of invasion
from without, and convulsions within. He has endeavoured to prevent the population of
these States; for that purpose obstructing the Laws for Naturalization of Foreigners;
refusing to pass others to encourage their migrations hither, and raising the conditions
of new Appropriations of Lands. He has obstructed the Administration of Justice, by
refusing his Assent to Laws for establishing Judiciary powers. He has made Judges dependent
on his Will alone, for the tenure of their offices, and the amount and payment of their
salaries. He has erected a multitude of New Offices, and sent hither swarms of Officers
to harrass our people, and eat out their substance. He has kept among us, in times of peace,
Standing Armies without the Consent of our legislatures. He has affected to render the
Military independent of and superior to the Civil power. He has combined with others to
subject us to a jurisdiction foreign to our constitution, and unacknowledged by our laws;
giving his Assent to their Acts of pretended Legislation: For Quartering large bodies of
armed troops among us: For protecting them, by a mock Trial, from punishment for any
Murders which they should commit on the Inhabitants of these States: For cutting off our
Trade with all parts of the world: For imposing Taxes on us without our Consent: For
depriving us in many cases, of the benefits of Trial by Jury: For transporting us beyond
Seas to be tried for pretended offences: For abolishing the free System of English Laws
in a neighbouring Province, establishing therein an Arbitrary government, and enlarging
its Boundaries so as to render it at once an example and fit instrument for introducing
the same absolute rule into these Colonies: For taking away our Charters, abolishing our
most valuable Laws, and altering fundamentally the Forms of our Governments:
"""
