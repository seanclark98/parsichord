from typing import Any

from pyabc import Note, Tune as ABCTune

from parsichord.chords import ChordVoicing
from parsichord.utils import partition


class Tune(ABCTune):
    def __init__(self, *args: Any, **kwargs: Any):
        self._chords: dict[int, ChordVoicing] = dict()
        super().__init__(*args, **kwargs)

    @property
    def notes(self) -> list[Note]:
        i = 0
        notes = []
        for note in self.tokens:
            if not isinstance(note, Note):
                continue
            notes.extend([note, *[None] * (int(note.duration) - 1)])
            i += note.duration
        return notes

    @property
    def bars(self) -> list[list[Note]]:
        nsubdivisions = int(self.header["meter"].split("/")[0])
        return partition(self.notes, nsubdivisions)

    def chord(self, i: int) -> ChordVoicing | None:
        return self._chords.get(i, None)
