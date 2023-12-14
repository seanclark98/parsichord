from itertools import product
from typing import Iterable

from .constants import Interval, Note, Triad, triad_to_intervals


class Pitch:
    # note = "pitch-class" in musical set theory
    def __init__(self, note: Note, octave: int):
        self.note = note
        self.octave = octave

    class Meta:
        unique_together = ("note", "octave")

    def __str__(self):
        return f"{self.note.name}-{self.octave}"

    def __repr__(self):
        return f"<Pitch {self.note.name}{self.octave}>"

    def __add__(self, ivl):
        note = self.note + ivl
        value = self.note.value + ivl
        octave = self.octave + (value // 12)
        pitch = Pitch(note=note, octave=octave)
        return pitch


class ChordType:
    def __init__(self, name: str, base: Triad, seventh: Interval | None = None, extensions: list[Interval] | None = None):
        self.name = name
        self.base = base
        self.seventh = seventh
        self.extensions = extensions

    def __str__(self):
        return self.name

    @property
    def intervals(self) -> list[Interval]:
        basechord = list(triad_to_intervals[self.base])
        seventh = [self.seventh] if self.seventh else []
        extensions = self.extensions or []
        intervals = basechord + seventh + extensions
        return intervals

    # @property
    # def relations(self) -> list["Relation"]:
    #     return self.ascending_relations.all() | self.descending_relations.all()


class Chord:
    def __init__(self, root: Note, chord_type: ChordType):
        self.root = root
        self.chord_type = chord_type
        self.notes = frozenset([root + ivl for ivl in chord_type.intervals])

    # class Meta:
    #     unique_together = ("root", "chord_type")

    def __str__(self):
        return f"{self.root.name} {self.chord_type.name}"

    def __repr__(self):
        return f"<Chord {self.root.name} {self.chord_type.name}>"

    def __add__(self, interval: int) -> "Chord":
        return Chord(
            root=self.root + interval, chord_type=self.chord_type
        )

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
        self.notes = set(self.root + ivl for ivl in self.chord_type.intervals)

    def parsimonious_chords(self) -> set["Chord"]:
        n = len(self.notes)
        chords = set()
        notes_list = list(self.notes)
        for i in range(n):
            for ivl in [-2, -1, 1, 2]:
                notes_copy = notes_list[:]
                notes_copy[i] += ivl
                chord = Chord.from_notes(notes=set(notes_copy))
                if chord:
                    chords.add(chord)
        return chords

    @staticmethod
    def from_notes(notes: Iterable) -> "Chord | None":
        for chord in triads:
            if set(chord.notes) == set(notes):
                return chord
        return None


triads = []

for root, triad in product(list(Note), list(Triad)):
    chord_type = ChordType(name=triad.value, base=triad)
    triads.append(Chord(root, chord_type))


class Relation:
    def __init__(self, name: str, chord_type_a: ChordType, chord_type_b: ChordType, transposition: Interval):
        self.name = name
        self.chord_type_a = chord_type_a
        self.chord_type_b = chord_type_b
        self.transposition = transposition

    def __call__(self, chord: Chord) -> Chord:
        if chord.chord_type == self.chord_type_a:
            return Chord(
                root=chord.root + self.transposition, chord_type=self.chord_type_b
            )
        elif chord.chord_type == self.chord_type_b:
            return Chord(
                root=chord.root - self.transposition, chord_type=self.chord_type_a
            )
        return chord

    def __str__(self):
        return self.name


class ChordVoicing:
    def __init__(self, chord: Chord, pitches: list[Pitch]):
        self.chord = chord
        self.pitches = frozenset(pitches)
        self.validate_pitches()

    # TODO: make chord voicing hashable

    def __eq__(self, other):
        if self.chord != other.chord:
            return False
        if self.pitches != other.pitches:
            return False
        return True

    def find_closest_voicings(self) -> set["ChordVoicing"]:
        n = len(self.pitches)
        voicings = set()
        pitches_list = list(self.pitches)
        for i in range(n):
            for ivl in [-2, -1, 1, 2]:
                pitches_copy = pitches_list[:]
                pitches_copy[i] += ivl
                chord = Chord.from_notes([pitch.note for pitch in pitches_copy])
                if not chord:
                    continue
                voicing = ChordVoicing(chord, pitches_copy)
                if voicing:
                    voicings.add(voicing)
        return voicings

    def validate_pitches(self):
        missing_notes = [
            note.name for note in self.chord.notes
            if note not in [pitch.note for pitch in self.pitches]
        ]
        if missing_notes:
            raise ValueError(
                f"Each note in {self.chord} must have a "
                "corresponding pitch in the chord voicing. "
                f"Missing notes: {missing_notes}"
            )

        invalid_pitches = [
            str(pitch) for pitch in self.pitches
            if pitch.note not in self.chord.notes
        ]
        if invalid_pitches:
            raise ValueError(
                f"Invalid pitches: {invalid_pitches}. "
                f"Each pitch must correspond to a note in {str(self.chord)} ({self.chord.notes})"
            )

    def __repr__(self):
        return f"<ChordVoicing {self.chord} {self.pitches}"