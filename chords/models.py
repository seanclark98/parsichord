from typing import Callable, Set

# from multiselectfield import MultiSelectField

from django.db import models

from chords.fields import Note, NoteField, Interval, IntervalsField


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


class ChordType(models.Model):
    name = models.CharField(max_length=30)
    intervals = IntervalsField(choices=Interval.choices, max_length=12)

    def __str__(self):
        return self.name


class Chord(models.Model):
    root = NoteField(choices=Note.choices)
    chord_type = models.ForeignKey(ChordType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.root.name} {self.chord_type.name}"

    @property
    def notes(self):
        return [self.root] + [self.root + ivl for ivl in self.chord_type.intervals]

    @property
    def related_chords(self, relation: Callable) -> Set:
        return {}

    # @property
    # def intervals(self):
    #     if self._intervals:
    #         return self._intervals

    #     self._intervals = []
    #     previous_note = self.notes[0]
    #     for note in self.notes:
    #         ivl = (note.value - previous_note.value) % 12
    #         self._intervals.append(ivl)
    #         previous_note = note
    #     return self._intervals


# def sub_v(chord: Chord) -> Chord:
#     chord

# class Chord():
#     notes = models.ManyToManyField(Pitch)
