from dataclasses import dataclass
from enum import Enum, auto

from parsichord.utils import partition

from .cadence import Cadence
from .tune import Tune


class PhraseType(Enum):
    ANTECEDENT = auto()
    CONSEQUENT = auto()


@dataclass(frozen=True)
class PhraseSpan:
    """Represents a phrase and its position within the tune."""

    phrase_type: PhraseType
    start: int
    end: int


class TuneStructure:
    """Represents the formal structure of a tune, with non-overlapping phrases
    of regular length."""

    def __init__(self, tune: Tune, phrase_length_in_bars: int) -> None:
        self.tune: Tune = tune
        self.length: int = len(tune.notes)
        self.phrase_length: int = phrase_length_in_bars * 8
        self.phrases: list[PhraseSpan] = []
        self._analyze_form()

    def add_phrase(self, phrase_type: PhraseType, start: int, end: int) -> None:
        """Add a phrase to the structure."""
        if not (0 <= start < end <= self.length):
            raise ValueError(
                f"Invalid phrase bounds: {start}-{end} for tune of length {self.length}"
            )

        if end - start + 1 != self.phrase_length:
            raise ValueError(f"Phrase length must be {self.phrase_length}")

        expected_start = len(self.phrases) * self.phrase_length
        if start != expected_start:
            raise ValueError(f"Phrase must start at position {expected_start}")

        self.phrases.append(PhraseSpan(phrase_type, start, end))

    def get_phrase_type_at(self, position: int) -> PhraseType | None:
        """Get the phrase type at the given position."""
        if not (0 <= position < self.length):
            raise ValueError(
                f"Position {position} out of bounds for tune of length {self.length}"
            )

        phrase_index = position // self.phrase_length
        if phrase_index < len(self.phrases):
            return self.phrases[phrase_index].phrase_type
        return None

    def _detect_periods(self) -> None:
        """Detect periods in the tune."""
        phrases = partition(self.tune.notes, part_size=self.phrase_length)
        for i, current_phrase in enumerate(phrases[:-1]):
            next_phrase = phrases[i + 1]
            if current_phrase[:4] == next_phrase[:4]:
                self.add_phrase(
                    PhraseType.ANTECEDENT,
                    i * self.phrase_length,
                    (i + 1) * self.phrase_length - 1,
                )
                self.add_phrase(
                    PhraseType.CONSEQUENT,
                    (i + 1) * self.phrase_length,
                    (i + 2) * self.phrase_length - 1,
                )

    def _analyze_form(self) -> None:
        """Analyze the tune's form and populate phrases."""
        self._detect_periods()


def suggest_cadence(tune: Tune, position: int) -> Cadence:
    """Suggest a cadence based on the tune's structure at the given
    position."""
    # structure = TuneStructure(tune, phrase_length_in_bars=4)
    # phrase_type = structure.get_phrase_type_at(position)

    # Cadence selection logic based on phrase_type
    return NotImplemented
