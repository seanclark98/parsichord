from pyabc import ChordBracket, ChordSymbol, Note as ABCNote, Token, Tune as ABCTune

from parsichord.core.chord import ChordVoicing, Pitch
from parsichord.core.tune import Note, Tune
from parsichord.data.thesession import TuneData
from parsichord.utils import partition


def chord_voicing_tokens(token: Token, chord_voicing: ChordVoicing) -> list[Token]:
    pitches = sorted(chord_voicing.pitches, key=lambda p: p.abs_value)
    chord_open_bracket = ChordBracket(line=token._line, char=token._char, text="[")
    chord_closed_bracket = ChordBracket(line=token._line, char=token._char, text="]")
    return [chord_open_bracket, *pitches, chord_closed_bracket]


def create_chord_symbol(token: Token, chord_voicing: ChordVoicing) -> ChordSymbol:
    return ChordSymbol(
        line=token._line, char=token._char, text=f'"{chord_voicing.chord}"'
    )


def chord_tokens(token: Token, chord_voicing: ChordVoicing) -> list[Token]:
    chord_symbol = create_chord_symbol(token, chord_voicing)
    return [chord_symbol, *chord_voicing_tokens(token, chord_voicing)]


class PyABCNoteAdapter(Note):
    def __init__(self, pyabc_note: ABCNote):
        self._note = pyabc_note

    @property
    def pitch(self) -> Pitch:
        acc = self._note.key.accidentals.get(self._note.note[0].upper(), "")
        name = self._note.note.upper() + acc
        value = self._note.pitch.pitch_value(name)
        return Pitch(value=value)

    @property
    def duration(self) -> float:
        return self._note.duration


class PyABCTuneAdapter(Tune):
    def __init__(self, tune_data: TuneData):
        super().__init__()
        self._tune = self._load_pyabc_tune(tune_data)

    def _load_pyabc_tune(self, tune_data: TuneData) -> ABCTune:
        return ABCTune(json=tune_data)

    @property
    def notes(self) -> list[Note | None]:
        i = 0
        notes = []
        for abcnote in self._tune.tokens:
            if not isinstance(abcnote, ABCNote):
                continue
            note: Note = PyABCNoteAdapter(abcnote)
            notes.extend([note, *[None] * (int(note.duration) - 1)])
            i += int(note.duration)
        return notes

    @property
    def bars(self) -> list[list[Note | None]]:
        nsubdivisions = int(self._tune.header["meter"].split("/")[0])
        return partition(self.notes, nsubdivisions)
