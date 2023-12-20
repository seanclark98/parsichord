from parsichord.chords import Chord, ChordType, Major, Minor
from parsichord.constants import Interval


class Transformation:
    def __init__(
        self,
        chord_type_a: ChordType,
        chord_type_b: ChordType,
        transposition: Interval,
    ):
        self.chord_type_a = chord_type_a
        self.chord_type_b = chord_type_b
        self.transposition = transposition

    def __call__(self, chord: Chord) -> Chord:
        if chord.chord_type == self.chord_type_a:
            return Chord(
                root=chord.root + self.transposition, chord_type=self.chord_type_b
            )
        if chord.chord_type == self.chord_type_b:
            return Chord(
                root=chord.root - self.transposition, chord_type=self.chord_type_a
            )
        return chord


P = Transformation(Major, Minor, Interval.PERFECT_FIRST)
L = Transformation(Minor, Major, Interval.PERFECT_FOURTH)
R = Transformation(Minor, Major, Interval.MAJOR_SIXTH)
plr_group: list[Transformation] = [P, L, R]


def alternate_subdominant(chord: Chord) -> Chord:
    if chord.is_major() and chord.is_triad():
        return chord + Interval.MAJOR_SECOND
    raise NotImplementedError


def primary_subdominant(chord: Chord) -> Chord:
    if chord.is_major() and chord.is_triad():
        return chord + Interval.PERFECT_FOURTH
    raise NotImplementedError


def dominant(chord: Chord) -> Chord:
    if chord.is_major() and chord.is_triad():
        return chord + Interval.PERFECT_FIFTH
    raise NotImplementedError


# def sub_v(chord: Chord) -> Chord:
#     chord
