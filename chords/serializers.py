from rest_framework import serializers

from chords.models import Chord, Note, Scale


class ChordSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Chord
        fields = ("name", "notes")

    def get_notes(self, chord):
        return [Note(n).name for n in chord.notes]


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = ("name", "notes")
