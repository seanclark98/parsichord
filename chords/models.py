from __future__ import annotations

from django.db import models

from .constants import Interval, Note, Triad, TriadIntervals
from .fields import NoteField, IntervalField, IntervalsField


class Pitch(models.Model):
    # note = "pitch-class" in musical set theory
    note = NoteField(choices=Note.choices)
    octave = models.IntegerField()
    audio = models.FileField(upload_to="audio/", null=True, blank=True)

    class Meta:
        unique_together = ("note", "octave")

    def __str__(self):
        return f"{self.note.name}-{self.octave}"


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
    base = models.CharField(choices=Triad.choices, max_length=30)
    seventh = IntervalField(choices=Interval.choices, null=True, blank=True)
    extensions = IntervalsField(
        choices=Interval.choices, max_length=12, blank=True
    )

    def __str__(self):
        return self.name

    @property
    def intervals(self) -> list[Interval]:
        basechord = list(TriadIntervals[self.base].value)
        seventh = [self.seventh] if self.seventh else []
        intervals = basechord + seventh + self.extensions
        return intervals

    @property
    def relations(self) -> models.QuerySet[Relation]:
        return self.ascending_relations.all() | self.descending_relations.all()


class Chord(models.Model):
    root = NoteField(choices=Note.choices)
    chord_type = models.ForeignKey(ChordType, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("root", "chord_type")

    def __str__(self):
        return f"{self.root.name} {self.chord_type.name}"

    def __add__(self, interval: int) -> Chord:
        new_chord, _ = Chord.objects.get_or_create(
            root=self.root + interval, chord_type=self.chord_type
        )
        return new_chord

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, interval: Interval) -> Note | None:
        return note if (note := self.root + interval) in self.notes else None

    def is_major(self) -> bool:
        return self.root + Interval.MAJOR_THIRD in self.notes

    def is_minor(self) -> bool:
        return self.root + Interval.MINOR_THIRD in self.notes

    def is_tertian(self) -> bool:
        return all(
            [
                ivl in [Interval.MINOR_THIRD, Interval.MAJOR_THIRD]
                for ivl in self.chord_type.intervals
            ]
        )

    def is_triad(self) -> bool:
        return self.is_tertian and len(self) == 3

    @property
    def notes(self) -> list[Note]:
        return [self.root + ivl for ivl in self.chord_type.intervals]


class Relation(models.Model):
    name = models.CharField(max_length=30)
    chord_type_a = models.ForeignKey(
        ChordType, on_delete=models.CASCADE, related_name="ascending_relations"
    )
    chord_type_b = models.ForeignKey(
        ChordType, on_delete=models.CASCADE, related_name="descending_relations"
    )
    transposition = IntervalField()

    def __call__(self, chord: Chord) -> Chord:
        new_chord = chord
        if chord.chord_type == self.chord_type_a:
            new_chord, _ = Chord.objects.get_or_create(
                root=chord.root + self.transposition, chord_type=self.chord_type_b
            )
        elif chord.chord_type == self.chord_type_b:
            new_chord, _ = Chord.objects.get_or_create(
                root=chord.root - self.transposition, chord_type=self.chord_type_a
            )
        return new_chord

    def __str__(self):
        return self.name


class ChordVoicing(models.Model):
    chord = models.ForeignKey(Chord, on_delete=models.CASCADE, related_name="voicings")
    pitches = models.ManyToManyField(Pitch)
