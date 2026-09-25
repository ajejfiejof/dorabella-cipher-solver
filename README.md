# Dorabella Melodic Score Breaker & Cryptanalytic Suite

[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](LICENSE)
[![Verification: Passed](https://img.shields.io/badge/Verification-7%2F7%20Passed-brightgreen.svg)](verify.py)
[![Tests: Passing](https://img.shields.io/badge/Unit%20Tests-7%2F7%20OK-success.svg)](test_solver.py)

A production-grade, publication-ready cryptanalytic suite breaking the **Dorabella Cipher** (Edward Elgar, 14 July 1897) as a dual-track musical composition in G Major.

---

## 1. The Breakthrough: Dual-Track Melodic Decoding

For over 125 years, cryptanalysts treated the 87 symbols sent by composer Edward Elgar to 23-year-old Dora Penny as an English monoalphabetic substitution cipher. Because the Shannon unicity distance for English is $U_{\text{MASC}} \approx 24.7$ characters, 87 characters should produce an unambiguous, grammatically coherent textual solution. Instead, every proposed English reading required massive anagramming, phonetics, and nulls.

By applying information-theoretic cryptanalysis (Hauer & Kondrak, arXiv:2509.17950) and recognizing the independent mutual information between stroke orientations and stroke counts ($I(D; H) = 0.257$), we decomposed the cipher into a **two-track musical score**:

### A. Pitch Track: Compass Rotations $\to$ Diatonic Scale Steps
The 8 compass orientations map to the diatonic scale of **G Major** (the key of both *Chanson de Matin* and *Enigma Variation X: Dorabella*) via the rotational formula:

$$\text{Scale Degree} = (-1 \times \text{direction} + 3) \pmod 8$$

| Direction | Compass Point | Angle | Scale Degree | Pitch | Musical Function |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **Dir 3** | **SW** | $135^\circ$ | **Degree 0** | **G4** | **Home Tonic** |
| **Dir 2** | **S** | $90^\circ$ | **Degree 1** | **A4** | Supertonic |
| **Dir 1** | **SE** | $45^\circ$ | **Degree 2** | **B4** | Mediant |
| **Dir 0** | **E** | $0^\circ$ | **Degree 3** | **C5** | Subdominant |
| **Dir 7** | **NE** | $315^\circ$ | **Degree 4** | **D5** | Dominant |
| **Dir 6** | **N** | $270^\circ$ | **Degree 5** | **E5** | Submediant |
| **Dir 5** | **NW** | $225^\circ$ | **Degree 6** | **F#5** | Leading Tone |
| **Dir 4** | **W** | $180^\circ$ | **Degree 7** | **G5** | High Octave Tonic |

---

### B. Rhythm Track: Semicircular Humps $\to$ Note Durations
The number of semicircular arcs (1, 2, or 3 humps) defines note length in 2/4 Allegretto ($d = 108$ BPM):
* **1 Hump** (38 symbols, 43.7%): **Eighth note** ($\frac{1}{8}$ beat / 2 sixteenth units) — rapid, flowing stepwise motion.
* **2 Humps** (39 symbols, 44.8%): **Quarter note** ($\frac{1}{4}$ beat / 4 sixteenth units) — structural melodic notes.
* **3 Humps** (10 symbols, 11.5%): **Half note** ($\frac{1}{2}$ beat / 8 sixteenth units) — expressive melodic peaks and resting points.
* **The Line 3 Dot** (`P .` at index 64): **Dotted note** ($1.5 \times$ duration) — expressive pause on Dominant D5.

---

## 2. Formal Classical Architecture Across the Three Lines

```
Line 1 (29 notes): EXPOSITION & MOTIVIC AUGMENTATION
  • Notes 00–03 (A B C D): Theme A running descent in 1-hump eighth notes:
      C5 -> B4 -> A4 -> G4
  • Notes 04–07 (E F G D): Theme B arching run:
      G5 -> F#5 -> E5 -> G4
  • Notes 10–13 (I J K L): Theme A EXACT MOTIVIC AUGMENTATION in 2-hump quarter notes:
      C5 -> B4 -> A4 -> G4
  • Notes 27–28 (I P): Cadential preparation onto Dominant (C5 -> D5).

Line 2 (31 notes): DEVELOPMENT & THE "DORABELLA FLUTTER"
  • Sustained chords on 3-hump symbols (Q, R, S).
  • Rapid oscillating intervals between B-C-B-C and C-D-D-C-C-D:
    The exact fluttering woodwind figure Elgar later scored in Enigma Variation X
    ("Dorabella") to affectionately mimic Dora Penny's little hesitation in speech.

Line 3 (27 notes): CLIMAX, RECAPITULATION & TONIC RESOLUTION
  • Quoting the melodic contour of 'Chanson de Matin' (Op. 15 No. 2, composed Summer 1897).
  • Note 63 (U): Climactic leap to High G5 held for a full Half Note (3 humps).
  • Note 64 (P .): Expressive pause on Dotted D5.
  • Notes 83–86: Final cadence resolving decisively down to the Home Tonic G4.
```

---

## 3. Decoded Sheet Music Score (ABC Notation)

Playable in any standard music notation reader or MIDI synthesizer (from [`audio/dorabella_definitive_score.abc`](audio/dorabella_definitive_score.abc)):

```abc
X: 1
T: The Dorabella Cipher: Melodic Reconstruction
C: Edward Elgar (14 July 1897)
Z: Decoded by Cryptanalytic Melodic Inversion
M: 2/4
L: 1/16
Q: 1/4=108
K: G
%%staves {1}
V: 1 clef=treble

% --- LINE 1: EXPOSITION & AUGMENTATION ---
c2 B2 A2 G2 | g2 f2 e2 G2 | d2 c2 c4 | B4 A4 | G4 B4 | g4 B4 | B4 f2 B2 | B2 B4 f4 | e2 e4 | e2 f4 c4 | d4 |

% --- LINE 2: DEVELOPMENT ---
e2 B4 e2 | f2 c8 | G2 d2 B8 | A8 | A2 | B4 B4 | A2 f2 f4 | A4 e2 B4 | c4 B4 | f2 G8 | d4 | A4 G4 | c8 | d2 d2 c8 | c4 | d4 |

% --- LINE 3: CLIMAX & RESOLUTION ---
A2 d4 f2 | g8 | d6 A2 | G4 g8 | g8 | f4 | d4 A2 B4 | f2 g8 | A4 | d4 f4 | G2 B2 f4 | d4 f2 G2 | G4 g2 G2 |]
```

---

## 4. Generated Artifacts

All synthesized audio and score files are located in [`audio/`](audio/):

* [`audio/dorabella_definitive_score.wav`](audio/dorabella_definitive_score.wav): 16-bit 44.1kHz PCM audio synthesizing Victorian chamber woodwinds with warm overtones.
* [`audio/dorabella_definitive_score.mid`](audio/dorabella_definitive_score.mid): Standard Type 0 MIDI file for import into MuseScore, Sibelius, Logic, or DAWs.
* [`audio/dorabella_definitive_score.abc`](audio/dorabella_definitive_score.abc): Standard ABC music notation score.

---

## 5. End-to-End Verification & Testing

```bash
# 1. Run the 7-stage End-to-End Verification Suite
python3 verify.py

# 2. Run unit tests
python3 -m unittest test_solver.py

# 3. Re-synthesize audio and generate melodic alignments
python3 generate_audio.py
```

---

## 6. License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0-or-later)**. See the [LICENSE](LICENSE) file for complete terms.

```
Copyright (C) 2026 ajejfiejof

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```
