from dataclasses import dataclass

from parsichord.core.chord import Major, ScaleDegreeChord
from parsichord.core.constants import Interval

cadences: dict[tuple[Interval, Interval, bool], "Cadence"] = dict()


@dataclass(frozen=True)
class Cadence:
    approach_note: Interval
    resolution_note: Interval
    approach_chord: ScaleDegreeChord
    resolution_chord: ScaleDegreeChord
    strong: bool

    def __post_init__(self) -> None:
        global cadences
        cadences[self.approach_note, self.resolution_note, self.strong] = self


perfect_cadence = Cadence(
    approach_note=Interval.MAJOR_SEVENTH,
    resolution_note=Interval.PERFECT_FIRST,
    approach_chord=ScaleDegreeChord(Interval.PERFECT_FIFTH, Major),
    resolution_chord=ScaleDegreeChord(Interval.PERFECT_FIRST, Major),
    strong=True,
)
imperfect_cadence = Cadence(
    approach_note=Interval.MAJOR_SEVENTH,
    resolution_note=Interval.PERFECT_FIRST,
    approach_chord=ScaleDegreeChord(Interval.PERFECT_FIFTH, Major),
    resolution_chord=ScaleDegreeChord(Interval.MAJOR_SIXTH, Major),
    strong=False,
)


def find_cadence(
    approach_note: Interval, resolution_note: Interval, strong: bool
) -> Cadence | None:
    return cadences.get((approach_note, resolution_note, strong), None)
