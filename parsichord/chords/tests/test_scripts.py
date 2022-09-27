"""Tests for scripts."""
from django.test import TestCase

from ..constants import Note
from ..models import Pitch
from ..scripts.create_pitches import create_pitches


class ScriptTests(TestCase):
    """Test scripts."""

    def test_create_pitches(self):
        create_pitches()
        self.assertEqual(Pitch.objects.count(), 4 * 12)
        self.assertEqual(Pitch.objects.filter(octave=3).count(), 12)
        self.assertEqual(Pitch.objects.last().note, Note.Eb)
        self.assertEqual(Pitch.objects.last().octave, 6)
