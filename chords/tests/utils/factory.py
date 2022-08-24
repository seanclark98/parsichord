import factory

from chords import models
from chords.constants import Note, Triad


class ChordTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ChordType
        django_get_or_create = ("name", "base")

    name = "Major"
    base = Triad.MAJOR


class ChordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Chord
        django_get_or_create = ("root", "chord_type")

    root = Note.C
    chord_type = factory.SubFactory(ChordTypeFactory)


class PitchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Pitch
        django_get_or_create = ("note", "octave")

    note = Note.C
    octave = 4


class ChordVoicingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ChordVoicing

    chord = factory.SubFactory(ChordFactory)

    @factory.post_generation
    def pitches(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for pitch in extracted:
                self.pitches.add(pitch)


# class ChordRelation(factory.django.DjangoModelFactory):
#     class Meta:
#         model = models.Relation

#     chord_type_a = factory.SubFactory(ChordTypeFactory)
#     chord_type_b = factory.SubFactory(ChordTypeFactory)
#     transposition = 
