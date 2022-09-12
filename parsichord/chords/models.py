from __future__ import annotations

from django.db import models

from .constants import Interval, Note, Triad, TriadIntervals
from .fields import NoteField, NotesField, IntervalField, IntervalsField


class Pitch(models.Model):
    # note = "pitch-class" in musical set theory
    note = NoteField(choices=Note.choices)
    octave = models.IntegerField()
    audio = models.FileField(upload_to="audio/", null=True, blank=True)

    class Meta:
        unique_together = ("note", "octave")

    def __str__(self):
        return f"{self.note.name}-{self.octave}"

    def __add__(self, ivl):
        note = self.note + ivl
        value = self.note.value + ivl
        octave = self.octave + (value // 12)
        pitch, _ = Pitch.objects.get_or_create(note=note, octave=octave)
        return pitch


class Scale(models.Model):
    name = models.CharField(max_length=30)
    notes = models.JSONField(
        "Notes",
        default=lambda: [Note.C, Note.D, Note.E, Note.F, Note.G, Note.A, Note.B]
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
    extensions = IntervalsField(choices=Interval.choices, max_length=12, blank=True)

    def __str__(self):
        return self.name

    @property
    def intervals(self) -> list[Interval]:
        basechord = list(TriadIntervals[self.base].value)
        seventh = [self.seventh] if self.seventh else []
        extensions = self.extensions or []
        intervals = basechord + seventh + extensions
        return intervals

    @property
    def relations(self) -> models.QuerySet[Relation]:
        return self.ascending_relations.all() | self.descending_relations.all()


class Chord(models.Model):
    root = NoteField(choices=Note.choices)
    chord_type = models.ForeignKey(ChordType, on_delete=models.CASCADE)
    notes = NotesField(
        choices=Note.choices, max_length=12, editable=False, default=set()
    )

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

    def update_notes(self):
        notes = set()
        for ivl in self.chord_type.intervals:
            notes.add(self.root + ivl)
        self.notes = notes

    def save(self, *args, **kwargs):
        self.update_notes()
        super().save(*args, **kwargs)

    @property
    def parsimonious_chords(self) -> set[Chord]:
        n = len(self.notes)
        chords = set()
        notes_list = list(self.notes)
        for i in range(n):
            for ivl in [-2, -1, 1, 2]:
                notes_copy = notes_list[:]
                notes_copy[i] += ivl
                chord = Chord.objects.filter(notes=set(notes_copy)).first()
                if chord:
                    chords.add(chord)
        return chords


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

    def find_closest_voicings(self, chord: Chord) -> set[ChordVoicing]:
        n = len(self.pitches.all())
        voicings = set()
        pitches_list = list(self.pitches.all())
        for i in range(n):
            for ivl in [-2, -1, 1, 2]:
                pitches_copy = pitches_list[:]
                pitches_copy[i] += ivl
                voicing = get_voicings_by_pitches(pitches_copy).first()
                if voicing:
                    voicings.add(voicing)
        return voicings

    def find_closest_voicing(self, chord: Chord) -> ChordVoicing | None:
        closest_voicings = self.find_closest_voicings(chord)
        return closest_voicings.pop() if closest_voicings else None


def get_voicings_by_pitches(pitches: list[Pitch]) -> models.QuerySet[ChordVoicing]:
    qs = ChordVoicing.objects
    for pitch in pitches:
        qs = qs.filter(pitches=pitch)
    return qs
