import pytest

from parsichord.core.chords import Chord, ChordType, ChordVoicing, Pitch
from parsichord.core.constants import Interval, PitchClass, Triad


class TestPitchClasss:
    def test_note_transposition(self) -> None:
        assert PitchClass.C + Interval.PERFECT_FIFTH == PitchClass.G
        assert PitchClass.C - Interval.PERFECT_FIFTH == PitchClass.F


class TestChordType:
    @pytest.mark.parametrize(
        "chord_type,abbr",
        [
            (ChordType("", Triad.MAJOR, Interval.MAJOR_SEVENTH), "maj7"),
            (ChordType("", Triad.MAJOR, Interval.MINOR_SEVENTH), "7"),
            (ChordType("", Triad.MINOR, Interval.MAJOR_SEVENTH), "minM7"),
            (ChordType("", Triad.MINOR, Interval.MINOR_SEVENTH), "min7"),
            (ChordType("", Triad.DIMINISHED, Interval.MINOR_SEVENTH), "min7b5"),
            (ChordType("", Triad.DIMINISHED, Interval.MAJOR_SIXTH), "dim7"),
        ],
    )
    def test_abbr(self, chord_type: ChordType, abbr: str) -> None:
        assert chord_type.abbr == abbr


class TestChordVoicing:
    def setup(self) -> None:
        major = ChordType(name="Major", base=Triad.MAJOR)
        self.c_major = Chord(root=PitchClass.C, chord_type=major)
        pitch_classes = [PitchClass.C.value, PitchClass.E.value, PitchClass.G.value]
        pitches = [Pitch(value=pitch_class, octave=4) for pitch_class in pitch_classes]
        self.c_major_voicing = ChordVoicing(chord=self.c_major, pitches=pitches)

        minor = ChordType(name="Minor", base=Triad.MINOR)
        self.e_minor = Chord(root=PitchClass.E, chord_type=minor)
        pitches = [
            Pitch(value=PitchClass.E.value, octave=4),
            Pitch(value=PitchClass.G.value, octave=4),
            Pitch(value=PitchClass.B.value, octave=3),
        ]
        self.e_minor_voicing = ChordVoicing(chord=self.e_minor, pitches=pitches)

    def test_chord_voicing(self) -> None:
        assert self.c_major_voicing.chord == self.c_major

    def test_initialisation_fails_for_invalid_pitches(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            ChordVoicing(
                self.c_major,
                [
                    Pitch(value=PitchClass.C.value, octave=4),
                    Pitch(value=PitchClass.D.value, octave=4),
                ],
            )
        assert str(excinfo.value) == (
            f"Each note in {self.c_major} must have a "
            "corresponding pitch in the chord voicing. "
            f"Missing notes: ['E', 'G']"
        )

    def test_voice_leading(self) -> None:
        assert self.e_minor_voicing in self.c_major_voicing.find_closest_voicings()
