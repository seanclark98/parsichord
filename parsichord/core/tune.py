from abc import ABC, abstractmethod

from parsichord.core.chords import ChordVoicing, Pitch


class Note(ABC):
    @property
    @abstractmethod
    def pitch(self) -> Pitch:
        ...

    @property
    @abstractmethod
    def duration(self) -> float:
        ...


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

    def get_chord(self, playhead: int) -> ChordVoicing | None:
        return self._chords.get(playhead, None)

    def set_chord(self, playhead: int, chord: ChordVoicing) -> None:
        self._chords[playhead] = chord
