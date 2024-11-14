from pyabc import (
    Beam,
    ChordBracket,
    ChordSymbol,
    Key as PyABCKey,
    Note as PyABCNote,
    Token,
    Tune as PyABCTune,
)

from parsichord.core.chord import ChordVoicing, Pitch
from parsichord.core.constants import PitchClass
from parsichord.core.tune import Key, Note, Tune
from parsichord.data.thesession import TuneData


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
    def __init__(self, pyabc_note: PyABCNote):
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
        self._bars, self._anacrusis = self._parse_bars()

    def _load_pyabc_tune(self, tune_data: TuneData) -> PyABCTune:
        return PyABCTune(json=tune_data)

    @property
    def key(self) -> Key:
        pyabc_key = PyABCKey(self._tune.header["key"])
        return Key(PitchClass(pyabc_key.root.value), pyabc_key.mode)

    @property
    def notes(self) -> list[Note | None]:
        return [note for bar in self.bars for note in bar]

    def _parse_bars(self) -> tuple[list[list[Note | None]], list[Note | None] | None]:
        """Parse the tune tokens into bars using beams as bar delimiters."""
        i = 0
        all_bars: list[list[Note | None]] = []
        current_bar: list[Note | None] = []

        for token in self._tune.tokens:
            if isinstance(token, Beam) and current_bar:
                all_bars.append(current_bar)
                current_bar = []
            elif isinstance(token, PyABCNote):
                note: Note = PyABCNoteAdapter(token)
                current_bar.extend([note, *[None] * (int(note.duration) - 1)])
                i += int(note.duration)

        # Add the last bar if it exists
        if current_bar:
            all_bars.append(current_bar)

        # Check if the first bar is an anacrusis
        if len(all_bars) > 0:
            expected_bar_length = len(all_bars[1])
            if len(all_bars[0]) < expected_bar_length:
                return all_bars[1:], all_bars[0]

        return all_bars, None

    @property
    def anacrusis(self) -> list[Note | None] | None:
        """Returns the anacrusis bar if it exists, otherwise None."""
        return self._anacrusis

    @property
    def bars(self) -> list[list[Note | None]]:
        """Returns the full bars of the tune, excluding any anacrusis."""
        return self._bars
