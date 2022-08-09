from typing import Callable, Set

from django.db import models


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


class Pitch(models.Model):
    note = models.IntegerField(choices=Note.choices)
    octave = models.IntegerField()
    audio = models.FileField(upload_to="audio/")


class Scale(models.Model):
    name = models.CharField(max_length=30)
    notes = models.JSONField(
        "Notes", default=list([Note.C, Note.D, Note.E, Note.F, Note.G, Note.A, Note.B])
    )

    # def __init__(self):
    #     print("notes:", self.notes)
    #     self.iternotes = iter(self.notes)

    def __iter__(self):
        self.iternotes = iter(self.notes)
        return self

    def __next__(self):
        return next(self.iternotes)


class Chord(models.Model):
    # length = models.IntegerField()
    name = models.CharField(max_length=30)
    notes = models.JSONField()
    # related_chords = models.ManyToManyField()

    _intervals = None

    def __str__(self):
        return self.name

    @property
    def related_chords(self, relation: Callable) -> Set:
        return {}

    @property
    def intervals(self):
        if self._intervals:
            return self._intervals

        self._intervals = []
        previous_note = self.notes[0]
        for note in self.notes:
            ivl = (note.value - previous_note.value) % 12
            self._intervals.append(ivl)
            previous_note = note
        return self._intervals


# class Chord():
#     notes = models.ManyToManyField(Pitch)
