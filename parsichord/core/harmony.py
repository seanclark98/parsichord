from abc import ABC, abstractmethod
from collections import Counter, deque
from functools import lru_cache

from ..utils import partition
from .chord import Chord, ChordVoicing, Pitch
from .constants import PitchClass
from .tune import Tune


class NotFound(Exception):
    pass


@lru_cache
def nearest_parsimonious_chord_containing_pitch_class(
    chord: Chord, pitch_class: PitchClass
) -> Chord:
    queue: deque[Chord] = deque()
    seen = set()
    # implement bfs
    queue.append(chord)
    while queue:
        new_chord = queue.popleft()
        if pitch_class in new_chord.pitch_classes:
            return new_chord
        seen.add(new_chord)

        for parsimonious_chord in new_chord.parsimonious_chords():
            if parsimonious_chord not in seen:
                queue.append(parsimonious_chord)
    raise NotFound(f"No path from {chord} to Chord containing {pitch_class}")


@lru_cache
def nearest_parsimonious_chord_voicing_containing(
    chord_voicing: ChordVoicing, pitch: Pitch | list[Pitch]
) -> ChordVoicing:
    queue: deque[ChordVoicing] = deque()
    if isinstance(pitch, list | tuple):
        pitches = pitch
    else:
        pitches = [pitch]
    seen = set()
    # implement bfs
    queue.append(chord_voicing)
    while queue:
        new_chord_voicing = queue.popleft()
        if all(p.pitch_class in new_chord_voicing.chord.pitch_classes for p in pitches):
            return new_chord_voicing
        seen.add(new_chord_voicing.chord)

        for parsimonious_chord_voicing in new_chord_voicing.find_closest_voicings():
            if parsimonious_chord_voicing.chord not in seen:
                queue.append(parsimonious_chord_voicing)
    raise NotFound(f"No path from {chord_voicing} to ChordVoicing containing {pitch}")


class SimpleChordStrategy:
    def __init__(self, harmonic_rhythm: int = 1):
        # notes per chord
        self.harmonic_rhythm = harmonic_rhythm

    def harmonize(self, tune: Tune, chord: Chord | None) -> None:
        previous_chord = None

        for playhead, note in enumerate(tune.notes):
            if chord is None:
                return None
            if note is None:
                continue
            pitch_class = note.pitch.pitch_class
            chord = nearest_parsimonious_chord_containing_pitch_class(
                chord, pitch_class
            )
            if chord != previous_chord and playhead % self.harmonic_rhythm == 0:
                previous_chord = chord
                voicing = ChordVoicing(
                    chord,
                    [
                        Pitch(
                            pitch_class,
                            1 if pitch_class.value < chord.root.value else 0,
                        )
                        for pitch_class in chord.pitch_classes
                    ],
                )
                tune.set_chord(playhead, voicing)


class IHarmonisationStrategy(ABC):
    def __init__(self, harmonic_rhythm: int = 1):
        # notes per chord
        self.harmonic_rhythm = harmonic_rhythm

    @abstractmethod
    def harmonize(self, tune: Tune, chord_voicing: ChordVoicing) -> None:
        pass


class FirstNoteStrategy(IHarmonisationStrategy):
    def harmonize(self, tune: Tune, chord_voicing: ChordVoicing) -> None:
        previous_chord_voicing = None
        tune._chords.clear()

        for playhead, note in enumerate(tune.notes):
            if chord_voicing is None:
                raise
            if note is None:
                continue

            pitch = note.pitch
            chord_voicing = nearest_parsimonious_chord_voicing_containing(
                chord_voicing, pitch
            )
            if (
                chord_voicing != previous_chord_voicing
                and playhead % self.harmonic_rhythm == 0
            ):
                previous_chord_voicing = chord_voicing
                tune.set_chord(playhead, chord_voicing)


class CommonTonesStrategy(IHarmonisationStrategy):
    def harmonize(self, tune: Tune, chord_voicing: ChordVoicing) -> None:
        previous_chord_voicing = None
        tune._chords.clear()

        for i, group in enumerate(
            partition(tune.notes, part_size=self.harmonic_rhythm)
        ):
            if chord_voicing is None:
                raise
            pitches = [note.pitch for note in group if note is not None]

            count_pitches = Counter(pitches)
            pitches = sorted(count_pitches, key=lambda i: -count_pitches[i])[:3]

            while True:
                print(f"{pitches=}")
                try:
                    chord_voicing = nearest_parsimonious_chord_voicing_containing(
                        chord_voicing, tuple(pitches)
                    )
                    print(f"Found {chord_voicing.chord=}")
                    break
                except NotFound:
                    pitches.pop()

            if chord_voicing != previous_chord_voicing:
                previous_chord_voicing = chord_voicing
                tune.set_chord(i * self.harmonic_rhythm, chord_voicing)
