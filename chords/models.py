from typing import Callable, Set

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import Interval, Note
from .fields import NoteField, IntervalsField


class Pitch(models.Model):
    note = NoteField(choices=Note.choices)
    octave = models.IntegerField()
    audio = models.FileField(upload_to="audio/", null=True, blank=True)

    class Meta:
        unique_together = ("note", "octave")

    def __str__(self):
        return f"{self.note.name}{self.octave}"


class Scale(models.Model):
    name = models.CharField(max_length=30)
    notes = models.JSONField(
        "Notes", default=list([Note.C, Note.D, Note.E, Note.F, Note.G, Note.A, Note.B])
    )

    def __iter__(self):
        self.iternotes = iter(self.notes)
        return self

    def __next__(self):
        return next(self.iternotes)


class ChordType(models.Model):
    name = models.CharField(max_length=30, unique=True)
    intervals = IntervalsField(choices=Interval.choices, max_length=12)

    def __str__(self):
        return self.name


class Chord(models.Model):
    root = NoteField(choices=Note.choices)
    chord_type = models.ForeignKey(ChordType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("root", "chord_type")

    def __str__(self):
        return f"{self.root.name} {self.chord_type.name}"

    def __add__(self, interval: int):
        return [note + interval for note in self.notes]

    def __len__(self):
        return len(self.notes)

    def is_major(self):
        return self.root + Interval.MAJOR_THIRD in self.notes

    def is_minor(self):
        return self.root + Interval.MINOR_THIRD in self.notes

    def is_tertian(self):
        return [
            ivl in [Interval.MINOR_THIRD, Interval.MAJOR_THIRD]
            for ivl in self.chord_type.intervals
        ]

    _notes = None

    @property
    def notes(self):
        if not self._notes:
            self._notes = [self.root + ivl for ivl in self.chord_type.intervals]
        return self._notes

    @property
    def related_chords(self, relation: Callable) -> Set:
        return {}


class ChordVoicing(models.Model):
    chord = models.ForeignKey(Chord, on_delete=models.CASCADE, related_name="voicings")
    pitches = models.ManyToManyField(Pitch)

    # class Meta:
    #     unique_together = ("chord", "pitches")

    def clean(self):
        if not all([self.chord.notes in self.pitches.values_list("note", flat=True)]):
            ValidationError(
                _(
                    "Each note in the chord must have a "
                    "corresponding pitch in the chord voicing."
                )
            )
