from __future__ import annotations

from enum import Enum

from django.db import models


class Interval(models.IntegerChoices):
    PERFECT_FIRST = 0, "P1"
    MINOR_SECOND = 1, "m2"
    MAJOR_SECOND = 2, "M2"
    MINOR_THIRD = 3, "m3"
    MAJOR_THIRD = 4, "M3"
    PERFECT_FOURTH = 5, "P4"
    DIMINISHED_FIFTH = 6, "dim5"
    PERFECT_FIFTH = 7, "P5"
    # AUGMENTED_FIFTH = 7, "aug5"
    MINOR_SIXTH = 8, "m6"
    MAJOR_SIXTH = 9, "M6"
    # DIMINISHED_SEVENTH = 9, "dim7"
    MINOR_SEVENTH = 10, "m7"
    MAJOR_SEVENTH = 11, "M7"
    OCTAVE = 12, "(8)"
    MINOR_NINTH = 13, "m9"
    MAJOR_NINTH = 14, "M9"
    MINOR_TENTH = 15, "m10"
    MAJOR_TENTH = 16, "M10"
    PERFECT_ELEVENTH = 17, "P11"
    AUGMENTED_ELEVENTH = 18, "aug11"
    PERFECT_TWELTH = 19, "P12"
    MINOR_THIRTEENTH = 20, "m13"
    MAJOR_THIRTEENTH = 21, "M13"
    AUGMENTED_THIRTEENTH = 22, "aug13"

    def __add__(self, interval: int | Interval):
        ivl = interval.value if type(interval) is Interval else interval
        return Interval((self.value + ivl) % 12)

    def __sub__(self, interval: int | Interval):
        ivl = interval.value if type(interval) is Interval else interval
        return Interval((self.value - ivl) % 12)


class Note(models.IntegerChoices):
    C = 0
    Db = 1
    D = 2
    Eb = 3
    E = 4
    F = 5
    Gb = 6
    G = 7
    Ab = 8
    A = 9
    Bb = 10
    B = 11

    def __str__(self):
        return self.name

    def __add__(self, interval: int | Interval):
        if not type(interval) in [int, Interval]:
            raise TypeError("interval must be of type int or Interval.")
        return Note((self.value + interval) % 12)

    def __sub__(self, interval: int | Interval):
        if not type(interval) in [int, Interval]:
            raise TypeError("interval must be of type int or Interval.")
        return Note((self.value - interval) % 12)


class TriadIntervals(Enum):
    # fmt: off
    DIM = (
        Interval.PERFECT_FIRST, Interval.MINOR_THIRD, Interval.DIMINISHED_FIFTH
    )
    MIN = (
        Interval.PERFECT_FIRST, Interval.MINOR_THIRD, Interval.PERFECT_FIFTH
    )
    MAJ = (
        Interval.PERFECT_FIRST, Interval.MAJOR_THIRD, Interval.PERFECT_FIFTH
    )
    AUG = (
        Interval.PERFECT_FIRST, Interval.MAJOR_THIRD, Interval.MINOR_SIXTH
    )
    # fmt: on


class Triad(models.TextChoices):
    DIMINISHED = "DIM", "Diminished"
    MINOR = "MIN", "Minor"
    MAJOR = "MAJ", "Major"
    AUGMENTED = "AUG", "Augmented"


# class ChordBase(models.Choices):
#     DIMINISHED = Triad.DIMINISHED, "Diminished"
#     MINOR = Triad.MINOR, "Minor"
#     MAJOR = Triad.MAJOR, "Major"
#     AUGMENTED = Triad.AUGMENTED, "Augmented"
