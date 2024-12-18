from abc import ABC, abstractmethod

from parsichord.core.chord import ChordVoicing, Pitch
from parsichord.core.constants import PitchClass


class Note(ABC):
    @property
    @abstractmethod
    def pitch(self) -> Pitch:
        ...

    @property
    @abstractmethod
    def duration(self) -> float:
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.pitch}, {self.duration})"

    def __str__(self) -> str:
        return f"{self.pitch} {self.duration}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Note):
            return False
        return (
            self.pitch.abs_value == other.pitch.abs_value
            and self.duration == other.duration
        )


class Key:
    def __init__(self, tonic: PitchClass, mode: str):
        self.tonic = tonic
        self.mode = mode


class Tune(ABC):
    def __init__(self) -> None:
        self._chords: dict[int, ChordVoicing] = dict()

    @property
    @abstractmethod
    def notes(self) -> list[Note | None]:
        ...

    @property
    @abstractmethod
    def bars(self) -> list[list[Note | None]]:
        ...

    @property
    @abstractmethod
    def key(self) -> Key:
        ...

    def get_chord(self, playhead: int) -> ChordVoicing | None:
        return self._chords.get(playhead, None)

    def set_chord(self, playhead: int, chord: ChordVoicing) -> None:
        self._chords[playhead] = chord
