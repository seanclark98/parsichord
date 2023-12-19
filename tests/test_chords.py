import pytest

from parsichord.chords import Chord, ChordType, ChordVoicing, Pitch
from parsichord.constants import Interval, Note, Triad


class TestNotes:
    def test_note_transposition(self) -> None:
        assert Note.C + Interval.PERFECT_FIFTH == Note.G
        assert Note.C - Interval.PERFECT_FIFTH == Note.F


class TestChordVoicing:
    def setup(self) -> None:
        major = ChordType(name="Major", base=Triad.MAJOR)
        notes = [Note.C, Note.E, Note.G]
        self.c_major = Chord(root=Note.C, chord_type=major)
        pitches = [Pitch(note=note, octave=4) for note in notes]
        self.c_major_voicing = ChordVoicing(chord=self.c_major, pitches=pitches)

        minor = ChordType(name="Minor", base=Triad.MINOR)
        self.e_minor = Chord(root=Note.E, chord_type=minor)
        pitches = [
            Pitch(note=Note.E, octave=4),
            Pitch(note=Note.G, octave=4),
            Pitch(note=Note.B, octave=3),
        ]
        self.e_minor_voicing = ChordVoicing(chord=self.e_minor, pitches=pitches)

    def test_chord_voicing(self) -> None:
        assert self.c_major_voicing.chord == self.c_major

    def test_initialisation_fails_for_invalid_pitches(self) -> None:
        with pytest.raises(ValueError) as excinfo:
            ChordVoicing(
                self.c_major,
                [Pitch(note=Note.C, octave=4), Pitch(note=Note.D, octave=4)],
            )
        assert str(excinfo.value) == (
            f"Each note in {self.c_major} must have a "
            "corresponding pitch in the chord voicing. "
            f"Missing notes: ['E', 'G']"
        )

    def test_voice_leading(self) -> None:
        assert self.e_minor_voicing in self.c_major_voicing.find_closest_voicings()
