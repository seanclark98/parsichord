from rest_framework import serializers

from .models import Chord, ChordType, Scale

# from .utils.chord_relations import triad_transformations


class ChordTypeSerializer(serializers.ModelSerializer):
    # intervals = serializers.SerializerMethodField()

    class Meta:
        model = ChordType
        fields = ("name", "intervals")


# class RelatedChordSerializer(serializers.ModelSerializer):
#     root = serializers.SerializerMethodField()
#     chord_type = serializers.SerializerMethodField()

#     class Meta:
#         model = Chord
#         fields = ("root", "chord_type")

#     def get_root(self, chord: Chord) -> str:
#         return chord.root.name

#     def get_chord_type(self, chord: Chord) -> str:
#         return chord.chord_type.name


class ChordSerializer(serializers.ModelSerializer):
    root = serializers.SerializerMethodField()
    chord_type = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    related_chords = serializers.SerializerMethodField()

    class Meta:
        model = Chord
        fields = ("root", "chord_type", "notes", "related_chords")

    def get_root(self, chord: Chord) -> str:
        return chord.root.name

    def get_chord_type(self, chord: Chord) -> str:
        return chord.chord_type.name

    def get_notes(self, chord: Chord) -> list[str]:
        return [note.name for note in chord.notes]

    def get_related_chords(self, chord: Chord) -> list[str]:
        return [str(rel_chord) for rel_chord in chord.related_chords.all()]


class ScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scale
        fields = ("name", "notes")
