from rest_framework import serializers

from chords.models import Chord, ChordType, Scale


class ChordTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChordType
        fields = ("name", "intervals")


class ChordSerializer(serializers.ModelSerializer):
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Chord
        fields = ("root", "chord_type", "notes")

    def get_notes(self, chord):
        return [note.name for note in chord.notes]


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = ("name", "notes")
