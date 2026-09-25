"""
Dorabella Musical Interpretation & Audio Synthesis Engine

Maps the 87 Dorabella symbols to musical notation, pitch contours,
standard MIDI, and synthesized 16-bit PCM WAV audio.
"""

import math
import struct
import wave
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
from dorabella_data import DorabellaSymbol, get_dorabella_symbol_sequence


# Diatonic scale pitch maps (semitone offsets from C4 = 60)
SCALES = {
    # G Major (Key of Enigma Variation X: Dorabella): G4, A4, B4, C5, D5, E5, F#5, G5
    "G_MAJOR": [67, 69, 71, 72, 74, 76, 78, 79],
    # C Major (Pure Diatonic): C4, D4, E4, F4, G4, A4, B4, C5
    "C_MAJOR": [60, 62, 64, 65, 67, 69, 71, 72],
    # E-flat Major (Elgar's heroic key, e.g. Symphony No. 2): Eb4, F4, G4, Ab4, Bb4, C5, D5, Eb5
    "EB_MAJOR": [63, 65, 67, 68, 70, 72, 74, 75],
    # G Minor (Enigma Theme opening key): G4, A4, Bb4, C5, D5, Eb5, F5, G5
    "G_MINOR": [67, 69, 70, 72, 74, 75, 77, 79],
}

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midi_to_note_name(midi_num: int) -> str:
    octave = (midi_num // 12) - 1
    note = NOTE_NAMES[midi_num % 12]
    return f"{note}{octave}"


def midi_to_freq(midi_num: int) -> float:
    """A4 = 69 = 440.0 Hz"""
    return 440.0 * (2.0 ** ((midi_num - 69) / 12.0))


@dataclass
class MusicalNote:
    symbol_index: int
    char_code: str
    midi_pitch: int
    note_name: str
    freq: float
    duration_beats: float
    is_rest: bool = False


class DorabellaMusicEngine:

    def __init__(
        self,
        scale_name: str = "G_MAJOR",
        hump_mode: str = "duration",   # "duration", "octave", or "fixed"
        tempo_bpm: int = 120
    ):
        self.scale = SCALES.get(scale_name, SCALES["G_MAJOR"])
        self.scale_name = scale_name
        self.hump_mode = hump_mode
        self.tempo_bpm = tempo_bpm
        self.beat_sec = 60.0 / tempo_bpm

    def symbols_to_melody(self, symbols: List[DorabellaSymbol]) -> List[MusicalNote]:
        """Convert Dorabella symbols into a sequence of MusicalNote objects."""
        melody: List[MusicalNote] = []

        for idx, s in enumerate(symbols):
            # Direction (0..7) maps to scale degree
            scale_degree = s.direction % len(self.scale)
            base_midi = self.scale[scale_degree]

            if self.hump_mode == "octave":
                # 1 hump = octave 0, 2 humps = +12, 3 humps = +24
                midi_pitch = base_midi + (s.humps - 1) * 12
                duration_beats = 1.0
            elif self.hump_mode == "duration":
                # 1 hump = eighth (0.5 beats), 2 humps = quarter (1.0 beats), 3 humps = half (2.0 beats)
                dur_map = {1: 0.5, 2: 1.0, 3: 2.0}
                duration_beats = dur_map.get(s.humps, 1.0)
                midi_pitch = base_midi
            else:
                midi_pitch = base_midi
                duration_beats = 1.0

            # The Dot on Line 3 Char 5: make it a dotted note (1.5x) or insert pause
            if s.has_dot_after:
                duration_beats *= 1.5

            melody.append(MusicalNote(
                symbol_index=idx,
                char_code=s.char_code,
                midi_pitch=midi_pitch,
                note_name=midi_to_note_name(midi_pitch),
                freq=midi_to_freq(midi_pitch),
                duration_beats=duration_beats,
                is_rest=False
            ))

        return melody

    @staticmethod
    def calculate_parsons_code(notes: List[MusicalNote]) -> str:
        """
        Parsons Code for musical contours:
        * = initial note
        u = up (pitch higher than previous)
        d = down (pitch lower than previous)
        r = repeat (same pitch as previous)
        """
        if not notes:
            return ""
        code = ["*"]
        for i in range(1, len(notes)):
            prev_p = notes[i - 1].midi_pitch
            curr_p = notes[i].midi_pitch
            if curr_p > prev_p:
                code.append("u")
            elif curr_p < prev_p:
                code.append("d")
            else:
                code.append("r")
        return "".join(code)

    def export_wav(
        self,
        melody: List[MusicalNote],
        output_filepath: str,
        sample_rate: int = 44100
    ):
        """
        Synthesize high-quality 16-bit PCM WAV audio with warm overtone harmonics
        and smooth ADSR envelope (resembling a Victorian chamber woodwind/music-box).
        """
        raw_samples = []

        for note in melody:
            num_samples = int(note.duration_beats * self.beat_sec * sample_rate)
            attack = int(0.04 * sample_rate)
            release = int(0.06 * sample_rate)
            sustain_level = 0.8
            freq = note.freq

            for n in range(num_samples):
                # Envelope
                if n < attack:
                    env = (n / attack)
                elif n > num_samples - release:
                    env = sustain_level * ((num_samples - n) / release)
                else:
                    env = sustain_level

                t = n / sample_rate
                # Fundamental + 2nd harmonic + 3rd harmonic
                sample_val = (
                    0.60 * math.sin(2.0 * math.pi * freq * t) +
                    0.25 * math.sin(2.0 * math.pi * 2.0 * freq * t) +
                    0.15 * math.sin(2.0 * math.pi * 3.0 * freq * t)
                ) * env

                # Scale to 16-bit integer
                int_val = int(sample_val * 24000.0)
                int_val = max(-32768, min(32767, int_val))
                raw_samples.append(struct.pack('<h', int_val))

            # Small silence gap (articulation) between notes (10ms)
            gap_samples = int(0.015 * sample_rate)
            for _ in range(gap_samples):
                raw_samples.append(struct.pack('<h', 0))

        with wave.open(output_filepath, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(raw_samples))

    def export_midi(self, melody: List[MusicalNote], output_filepath: str):
        """
        Generate a valid Standard MIDI file (Type 0) in pure Python.
        """
        ticks_per_quarter = 480
        track_events = []

        def write_var_len(val: int) -> bytes:
            buf = bytearray()
            buf.append(val & 0x7F)
            val >>= 7
            while val > 0:
                buf.insert(0, (val & 0x7F) | 0x80)
                val >>= 7
            return bytes(buf)

        # Set Tempo meta-event (microseconds per quarter note)
        us_per_quarter = int(60_000_000 / self.tempo_bpm)
        tempo_event = b'\x00\xFF\x51\x03' + struct.pack('>I', us_per_quarter)[1:]
        track_events.append(tempo_event)

        for note in melody:
            dur_ticks = int(note.duration_beats * ticks_per_quarter)
            # Delta-time 0, Note-On: 0x90, note, velocity 80
            note_on = write_var_len(0) + bytes([0x90, note.midi_pitch, 80])
            # Delta-time dur_ticks, Note-Off: 0x80, note, velocity 0
            note_off = write_var_len(dur_ticks) + bytes([0x80, note.midi_pitch, 0])
            track_events.append(note_on)
            track_events.append(note_off)

        # End of Track event
        end_of_track = write_var_len(0) + b'\xFF\x2F\x00'
        track_events.append(end_of_track)

        track_data = b''.join(track_events)
        track_chunk = b'MTrk' + struct.pack('>I', len(track_data)) + track_data
        header_chunk = b'MThd' + struct.pack('>IHHH', 6, 0, 1, ticks_per_quarter)

        with open(output_filepath, 'wb') as f:
            f.write(header_chunk + track_chunk)

    def export_abc(self, melody: List[MusicalNote], title: str = "Dorabella Melody") -> str:
        """Export as ABC musical notation string."""
        abc = [
            f"X: 1",
            f"T: {title}",
            f"C: Edward Elgar (Deciphered Hypothesis)",
            f"M: 3/4",
            f"L: 1/8",
            f"Q: 1/4={self.tempo_bpm}",
            f"K: {self.scale_name.split('_')[0]}",
            ""
        ]
        
        # Convert notes to ABC format
        line_chars = []
        for i, n in enumerate(melody):
            base_char = n.note_name[0]
            octave = int(n.note_name[-1])
            if octave >= 5:
                abc_note = base_char.lower() + ("'" * (octave - 5))
            else:
                abc_note = base_char.upper() + ("," * (4 - octave))
                
            line_chars.append(abc_note)
            if (i + 1) % 12 == 0:
                line_chars.append(" | ")
            elif (i + 1) % 4 == 0:
                line_chars.append(" ")

        abc.append("".join(line_chars) + " |]")
        return "\n".join(abc)
