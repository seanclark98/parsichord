from typing import Callable

from chords.fields import Interval
from chords.models import Chord, ChordType


Transformation = Callable[[Chord], Chord]
transformations: list[Transformation] = []


def transformation(t: Transformation) -> Transformation:
    transformations.append(t)
    return t


@transformation
def p(chord: Chord, i: ChordType, j: ChordType) -> Chord:
    if chord.chord_type not in [i, j]:
        return chord

    trans_type = i if (chord.chord_type == j) else j
    return Chord.objects.get_or_create(root=chord.root, chord_type=trans_type)


def alternate_subdominant(chord: Chord) -> Chord:
    return chord + Interval.MAJOR_SECOND


def primary_subdominant(chord: Chord) -> Chord:
    return chord + Interval.PERFECT_FOURTH


def dominant(chord: Chord) -> Chord:
    if not chord.is_tertian():
        return None
    if chord.is_major() and len(chord) == 3:
        return chord + Interval.PERFECT_FIFTH


# def sub_v(chord: Chord) -> Chord:
#     chord
