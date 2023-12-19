from typing import Callable

from parsichord.chords import Chord, Major, Minor
from parsichord.constants import Interval

Transformation = Callable[[Chord], Chord]
triad_transformations: list[Transformation] = []


def triad_transformation(t: Transformation) -> Transformation:
    triad_transformations.append(t)
    return t


@triad_transformation
def p_transformaiton(chord: Chord) -> Chord:
    if chord.is_major():
        return Chord(root=chord.root, chord_type=Minor)
    if chord.is_minor():
        return Chord(root=chord.root, chord_type=Major)
    return chord


@triad_transformation
def l_transformaiton(chord: Chord) -> Chord:
    if chord.is_major():
        return Chord(root=chord.root - 4, chord_type=Minor)
    if chord.is_minor():
        return Chord(root=chord.root + 4, chord_type=Major)
    return chord


@triad_transformation
def r_transformaiton(chord: Chord) -> Chord:
    if chord.is_major():
        return Chord(root=chord.root - 9, chord_type=Minor)
    if chord.is_minor():
        return Chord(root=chord.root + 9, chord_type=Major)
    return chord


# def p(chord: Chord, i: ChordType, j: ChordType) -> Chord:
#     if chord.chord_type not in [i, j]:
#         return chord

#     trans_type = i if (chord.chord_type == j) else j
#     return Chord.objects.get_or_create(root=chord.root, chord_type=trans_type)


def alternate_subdominant(chord: Chord) -> Chord:
    return chord + Interval.MAJOR_SECOND


def primary_subdominant(chord: Chord) -> Chord:
    return chord + Interval.PERFECT_FOURTH


def dominant(chord: Chord) -> Chord | None:
    if not chord.is_tertian():
        return None
    if chord.is_major() and len(chord) == 3:
        return chord + Interval.PERFECT_FIFTH
    if chord.is_minor() and len(chord) == 3:
        return chord + Interval.PERFECT_FIFTH
    return None


# def sub_v(chord: Chord) -> Chord:
#     chord
