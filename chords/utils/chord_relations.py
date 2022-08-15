from __future__ import annotations
from typing import Callable

from chords.fields import Interval
from chords.models import Chord, ChordType


Transformation = Callable[[Chord], Chord]
triad_transformations: list[Transformation] = []


def triad_transformation(t: Transformation) -> Transformation:
    triad_transformations.append(t)
    return t


@triad_transformation
def p_transformaiton(chord: Chord) -> Chord:
    new_chord = chord
    if chord.is_major():
        new_chord, _ = Chord.objects.get_or_create(
            root=chord.root, chord_type=ChordType.objects.get(name="Minor")
        )
    elif chord.is_minor():
        new_chord, _ = Chord.objects.get_or_create(
            root=chord.root, chord_type=ChordType.objects.get(name="Major")
        )
    return new_chord


@triad_transformation
def l_transformaiton(chord: Chord) -> Chord:
    new_chord = chord
    if chord.is_major():
        new_chord, _ = Chord.objects.get_or_create(
            root=chord.root - 4, chord_type=ChordType.objects.get(name="Minor")
        )
    elif chord.is_minor():
        new_chord, _ = Chord.objects.get_or_create(
            root=chord.root + 4, chord_type=ChordType.objects.get(name="Major")
        )
    return new_chord


@triad_transformation
def r_transformaiton(chord: Chord) -> Chord:
    new_chord = chord
    if chord.is_major():
        new_chord, _ = Chord.objects.get_or_create(
            root=chord.root - 9, chord_type=ChordType.objects.get(name="Minor")
        )
    elif chord.is_minor():
        new_chord, _ = Chord.objects.get_or_create(
            root=chord.root + 9, chord_type=ChordType.objects.get(name="Major")
        )
    return new_chord


# def p(chord: Chord, i: ChordType, j: ChordType) -> Chord:
#     if chord.chord_type not in [i, j]:
#         return chord

#     trans_type = i if (chord.chord_type == j) else j
#     return Chord.objects.get_or_create(root=chord.root, chord_type=trans_type)


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
