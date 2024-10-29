from enum import Enum
from typing import overload


class Interval(Enum):
    PERFECT_FIRST = 0  # , "P1"
    MINOR_SECOND = 1  # , "m2"
    MAJOR_SECOND = 2  # , "M2"
    MINOR_THIRD = 3  # , "m3"
    MAJOR_THIRD = 4  # , "M3"
    PERFECT_FOURTH = 5  # , "P4"
    DIMINISHED_FIFTH = 6  # , "dim5"
    PERFECT_FIFTH = 7  # , "P5"
    # AUGMENTED_FIFTH = 7  # , "aug5"
    MINOR_SIXTH = 8  # , "m6"
    MAJOR_SIXTH = 9  # , "M6"
    # DIMINISHED_SEVENTH = 9  # , "dim7"
    MINOR_SEVENTH = 10  # , "m7"
    MAJOR_SEVENTH = 11  # , "M7"
    OCTAVE = 12  # , "(8)"
    MINOR_NINTH = 13  # , "m9"
    MAJOR_NINTH = 14  # , "M9"
    MINOR_TENTH = 15  # , "m10"
    MAJOR_TENTH = 16  # , "M10"
    PERFECT_ELEVENTH = 17  # , "P11"
    AUGMENTED_ELEVENTH = 18  # , "aug11"
    PERFECT_TWELTH = 19  # , "P12"
    MINOR_THIRTEENTH = 20  # , "m13"
    MAJOR_THIRTEENTH = 21  # , "M13"
    AUGMENTED_THIRTEENTH = 22  # , "aug13"

    def __add__(self, interval: "int | Interval") -> "Interval":
        if not isinstance(interval, int | Interval):
            raise TypeError("interval must be of type int or Interval.")
        ivl = interval.value if isinstance(interval, Interval) else interval
        return Interval((self.value + ivl) % 12)

    def __sub__(self, interval: "int | Interval") -> "Interval":
        if not isinstance(interval, int | Interval):
            raise TypeError("interval must be of type int or Interval.")
        ivl = interval.value if isinstance(interval, Interval) else interval
        return Interval((self.value - ivl) % 12)

    @property
    def abbr(self) -> str:
        abbreviations = [
            "P1",
            "m2",
            "M2",
            "m3",
            "M3",
            "P4",
            "dim5",
            "P5",
            # "aug5",
            "m6",
            "M6",
            # "dim7",
            "m7",
            "M7",
            "(8)",
            "m9",
            "M9",
            "m10",
            "M10",
            "P11",
            "aug11",
            "P12",
            "m13",
            "M13",
            "aug13",
        ]
        return abbreviations[self.value]


class PitchClass(Enum):
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

    def __str__(self) -> str:
        return self.name

    @overload
    def __sub__(self, other: "PitchClass") -> Interval:
        ...

    @overload
    def __sub__(self, other: Interval | int) -> "PitchClass":
        ...

    def __sub__(self, other: "int | Interval | PitchClass") -> "Interval | PitchClass":
        if not isinstance(other, int | Interval | PitchClass):
            raise TypeError("other must be of type int, Interval or PitchClass.")
        if isinstance(other, PitchClass):
            return Interval((self.value - other.value) % 12)
        ivl = other.value if isinstance(other, Interval) else other
        return PitchClass((self.value - ivl) % 12)

    @overload
    def __add__(self, other: "PitchClass") -> Interval:
        ...

    @overload
    def __add__(self, other: Interval | int) -> "PitchClass":
        ...

    def __add__(self, other: "int | Interval | PitchClass") -> "PitchClass | Interval":
        if not isinstance(other, int | Interval | PitchClass):
            raise TypeError("other must be of type int, Interval or PitchClass.")
        if isinstance(other, PitchClass):
            return Interval((self.value + other.value) % 12)
        ivl = other.value if isinstance(other, Interval) else other
        return PitchClass((self.value + ivl) % 12)


class Triad(Enum):
    DIMINISHED = "Diminished"
    MINOR = "Minor"
    MAJOR = "Major"
    AUGMENTED = "Augmented"


triad_to_intervals = {
    Triad.DIMINISHED: (
        Interval.PERFECT_FIRST,
        Interval.MINOR_THIRD,
        Interval.DIMINISHED_FIFTH,
    ),
    Triad.MINOR: (Interval.PERFECT_FIRST, Interval.MINOR_THIRD, Interval.PERFECT_FIFTH),
    Triad.MAJOR: (Interval.PERFECT_FIRST, Interval.MAJOR_THIRD, Interval.PERFECT_FIFTH),
    Triad.AUGMENTED: (
        Interval.PERFECT_FIRST,
        Interval.MAJOR_THIRD,
        Interval.MINOR_SIXTH,
    ),
}
