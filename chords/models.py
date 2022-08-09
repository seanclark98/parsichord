# from enum import IntEnum
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


# class Note(models.Model):

#     Name = models.IntegerChoices("Name", "C Db D Eb E F Gb G Ab A Bb B")
#     # Name = models.IntegerChoices("Name", "C C# D D# E F F# G G# A A# B")

#     note = models.IntegerField(choices=Name.choices)

# def __str__(self):
#     return self.note

# def __add__(self, interval: int):
#     obj, _ = Note.objects.get_or_create(note=(self.note.value + interval) % 12)
#     return obj


PITCHES = []


class Pitch(models.Model):
    pitch = models.CharField(max_length=5)
    audio = models.FileField(upload_to="audio/")
    note = models.IntegerField(choices=Note.choices)


class Scale(models.Model):
    def __init__(self, root: Note, ivls):
        self.start = root
        self.notes = iter([root + ivl for ivl in ivls])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.notes)


class AbstractChord(models.Model):
    length = models.IntegerField()
    name = models.CharField(max_length=30)
    # notes = models.JSONField()
    # notes = models.ManyToManyField(Note)
    # related_chords = models.ManyToManyField()

    _intervals = None

    @property
    def related_chords(self, relation: Callable) -> Set:
        return {self}

    @property
    def intervals(self):
        if not self._intervals:
            self._intervals = [NOTE_TO_INT[note] for note in self.notes]
        return self._intervals


# class Chord(AbstractChord):
#     notes = models.ManyToManyField(Pitch)
