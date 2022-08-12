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


class Note(models.IntegerChoices):
    C = 1
    Db = 2
    D = 3
    Eb = 4
    E = 5
    F = 6
    Gb = 7
    G = 8
    Ab = 9
    A = 10
    Bb = 11
    B = 12

    def __add__(self, interval: int):
        return Note((self.value + interval) % 12)
