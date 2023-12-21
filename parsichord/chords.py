from itertools import product
from typing import Iterable

from pyabc import Pitch as ABCPitch

from .constants import Interval, PitchClass, Triad, triad_to_intervals


class Pitch(ABCPitch):
    def __hash__(self) -> int:
        return hash((self.value, self.octave))

    def __add__(self, ivl: int) -> "Pitch":
        return Pitch(super().__add__(ivl))

    def __sub__(self, ivl: int) -> "Pitch":
        return Pitch(super().__sub__(ivl))

    @property
    def equivalent_flat(self) -> "Pitch":
        return Pitch(super().equivalent_flat())

    @property
    def equivalent_sharp(self) -> "Pitch":
        return Pitch(super().equivalent_sharp())

    @property
    def pitch_class(self) -> PitchClass:
        return PitchClass(self.value)

    @staticmethod
    def pitch_value(pitch: "Pitch", root: str = "C") -> "Pitch":
        return Pitch(super().pitch_value(pitch, root))


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


# Triads
Augmented = ChordType(name="Augmented", base=Triad.AUGMENTED)
Diminished = ChordType(name="Diminished", base=Triad.DIMINISHED)
Major = ChordType(name="Major", base=Triad.MAJOR)
Minor = ChordType(name="Minor", base=Triad.MINOR)


class Chord:
    def __init__(self, root: PitchClass, chord_type: ChordType):
        self.root = root
        self.chord_type = chord_type

    def __str__(self) -> str:
        return f"{self.root.name} {self.chord_type.name}"

    # def __repr__(self):
    #     return f"{self.root.name} {self.chord_type.name}"

    def __add__(self, interval: Interval | int) -> "Chord":
        return Chord(root=self.root + interval, chord_type=self.chord_type)

    def __len__(self) -> int:
        return len(self.pitch_classes)

    def __getitem__(self, interval: Interval) -> PitchClass | None:
        return (
            pitch_class
            if (pitch_class := self.root + interval) in self.pitch_classes
            else None
        )

    def is_major(self) -> bool:
        return self.root + Interval.MAJOR_THIRD in self.pitch_classes

    def is_minor(self) -> bool:
        return self.root + Interval.MINOR_THIRD in self.pitch_classes

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
        n = len(self.pitch_classes)
        chords = set()
        notes_list = list(self.pitch_classes)
        for i in range(n):
            for ivl in [
                -Interval.MAJOR_SECOND.value,
                -Interval.MINOR_SECOND.value,
                Interval.MINOR_SECOND.value,
                Interval.MAJOR_SECOND.value,
            ]:
                notes_copy = notes_list[:]
                notes_copy[i] += ivl
                chord = Chord.from_pitch_classes(pitch_classes=set(notes_copy))
                if chord:
                    chords.add(chord)
        return chords

    @property
    def pitch_classes(self) -> list[PitchClass]:
        return [self.root + ivl for ivl in self.chord_type.intervals]

    @staticmethod
    def from_pitch_classes(pitch_classes: Iterable) -> "Chord | None":
        for chord in triads:
            if set(chord.pitch_classes) == set(pitch_classes):
                return chord
        return None


triads = []

for root, triad in product(list(PitchClass), list(Triad)):
    chord_type = ChordType(name=triad.value, base=triad)
    triads.append(Chord(root, chord_type))


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
                pitches_copy: list = pitches_list[:]
                pitches_copy[i] += ivl
                chord = Chord.from_pitch_classes(
                    [pitch.pitch_class for pitch in pitches_copy]
                )
                if not chord:
                    continue
                voicing = ChordVoicing(chord, pitches_copy)
                if voicing:
                    voicings.add(voicing)
        return voicings

    def validate_pitches(self) -> None:
        missing_pitches = [
            pitch.name
            for pitch in self.chord.pitch_classes
            if pitch not in [pitch.pitch_class for pitch in self.pitches]
        ]
        if missing_pitches:
            raise ValueError(
                f"Each note in {self.chord} must have a "
                "corresponding pitch in the chord voicing. "
                f"Missing notes: {missing_pitches}"
            )

        invalid_pitches = [
            str(pitch)
            for pitch in self.pitches
            if pitch.pitch_class not in self.chord.pitch_classes
        ]
        if invalid_pitches:
            raise ValueError(
                f"Invalid pitches: {invalid_pitches}. "
                "Each pitch must correspond to a note in "
                f"{str(self.chord)} ({self.chord.pitch_classes})"
            )
