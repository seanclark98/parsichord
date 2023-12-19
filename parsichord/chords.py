from itertools import product
from typing import Iterable

from .constants import Interval, Note, Triad, triad_to_intervals


class Pitch:
    # note = "pitch-class" in musical set theory
    def __init__(self, note: Note, octave: int):
        self.note = note
        self.octave = octave

    def __str__(self) -> str:
        return f"{self.note.name}{self.octave}"

    def __repr__(self) -> str:
        return f"Pitch({self.note}, {self.octave})"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Pitch)
            and self.note == other.note
            and self.octave == other.octave
        )

    def __hash__(self) -> int:
        return hash((self.note, self.octave))

    def __add__(self, ivl: Interval | int) -> "Pitch":
        note = self.note + ivl
        ivl = ivl.value if isinstance(ivl, Interval) else ivl
        value = self.note.value + int(ivl)
        octave = self.octave + (value // 12)
        pitch = Pitch(note=note, octave=octave)
        return pitch


class ChordType:
    def __init__(
        self,
        name: str,
        base: Triad,
        seventh: Interval | None = None,
        extensions: list[Interval] | None = None,
    ):
        self.name = name
        self.base = base
        self.seventh = seventh
        self.extensions = extensions

    def __str__(self) -> str:
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


# Triads
Augmented = ChordType(name="Augmented", base=Triad.AUGMENTED)
Diminished = ChordType(name="Diminished", base=Triad.DIMINISHED)
Major = ChordType(name="Major", base=Triad.MAJOR)
Minor = ChordType(name="Minor", base=Triad.MINOR)


class Chord:
    def __init__(self, root: Note, chord_type: ChordType):
        self.root = root
        self.chord_type = chord_type
        # self.notes = frozenset([root + ivl for ivl in chord_type.intervals])

    @property
    def notes(self) -> list[Note]:
        return [self.root + ivl for ivl in self.chord_type.intervals]

    def __str__(self) -> str:
        return f"{self.root.name} {self.chord_type.name}"

    # def __repr__(self):
    #     return f"{self.root.name} {self.chord_type.name}"

    def __add__(self, interval: Interval | int) -> "Chord":
        return Chord(root=self.root + interval, chord_type=self.chord_type)

    def __len__(self) -> int:
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
        return self.is_tertian() and len(self) == 3

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
    def __init__(
        self,
        name: str,
        chord_type_a: ChordType,
        chord_type_b: ChordType,
        transposition: Interval,
    ):
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

    def __str__(self) -> str:
        return self.name


class ChordVoicing:
    def __init__(self, chord: Chord, pitches: list[Pitch]):
        self.chord = chord
        self.pitches = frozenset(pitches)
        self.validate_pitches()

    def __repr__(self) -> str:
        return f"{self.chord} {self.pitches}"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ChordVoicing) and set(self.pitches) == set(
            other.pitches
        )

    def __hash__(self) -> int:
        return hash(frozenset(self.pitches))

    def find_closest_voicings(self) -> set["ChordVoicing"]:
        n = len(self.pitches)
        voicings = set()
        pitches_list = list(self.pitches)
        for i in range(n):
            for ivl in [
                -Interval.MAJOR_SECOND.value,
                -Interval.MINOR_SECOND.value,
                Interval.MINOR_SECOND.value,
                Interval.MAJOR_SECOND.value,
            ]:
                pitches_copy = pitches_list[:]
                pitches_copy[i] += ivl
                chord = Chord.from_notes([pitch.note for pitch in pitches_copy])
                if not chord:
                    continue
                voicing = ChordVoicing(chord, pitches_copy)
                if voicing:
                    voicings.add(voicing)
        return voicings

    def validate_pitches(self) -> None:
        missing_notes = [
            note.name
            for note in self.chord.notes
            if note not in [pitch.note for pitch in self.pitches]
        ]
        if missing_notes:
            raise ValueError(
                f"Each note in {self.chord} must have a "
                "corresponding pitch in the chord voicing. "
                f"Missing notes: {missing_notes}"
            )

        invalid_pitches = [
            str(pitch) for pitch in self.pitches if pitch.note not in self.chord.notes
        ]
        if invalid_pitches:
            raise ValueError(
                f"Invalid pitches: {invalid_pitches}. "
                "Each pitch must correspond to a note in "
                f"{str(self.chord)} ({self.chord.notes})"
            )
