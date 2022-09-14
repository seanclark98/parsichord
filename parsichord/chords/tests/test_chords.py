from django.test import TestCase
from rest_framework.test import APITestCase

import chords.tests.utils.factory as factory
from ..constants import Note, Interval, Triad
from ..models import Scale


class TestNotes(TestCase):
    def test_note_transposition(self):
        self.assertEqual(Note.C + Interval.PERFECT_FIFTH, Note.G)
        self.assertEqual(Note.C - Interval.PERFECT_FIFTH, Note.F)


class TestScale(TestCase):
    def setUp(self):
        self.scale = Scale.objects.create(name="C Major")

    def test_scale_iteration(self):
        it_scale = iter(self.scale)
        self.assertEqual(next(it_scale), Note.C)
        self.assertEqual(next(it_scale), Note.D)


class TestChordView(APITestCase):
    def setUp(self):
        self.c_major = factory.ChordFactory.create()

    def test_get_chords(self):
        response = self.client.get("/api/chords/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], self.c_major.id)


class TestChordVoicing(TestCase):
    def setUp(self):
        self.c_major = factory.ChordFactory.create()
        pitches = [
            factory.PitchFactory.create(note=note) for note in [Note.C, Note.E, Note.G]
        ]
        self.chord_voicing = factory.ChordVoicingFactory.create(pitches=pitches)

        self.minor = factory.ChordTypeFactory.create(name="Minor", base=Triad.MINOR)
        self.e_minor = factory.ChordFactory.create(root=Note.E, chord_type=self.minor)
        pitches = [
            factory.PitchFactory.create(note=Note.E, octave=4),
            factory.PitchFactory.create(note=Note.G, octave=4),
            factory.PitchFactory.create(note=Note.B, octave=3),
        ]
        self.e_minor_voicing = factory.ChordVoicingFactory.create(
            chord=self.e_minor, pitches=pitches
        )

    def test_chord_voicing(self):
        self.assertEqual(self.chord_voicing.chord, self.c_major)

    def test_voice_leading(self):
        self.assertEqual(
            self.chord_voicing.find_closest_voicing(self.e_minor), self.e_minor_voicing
        )
