from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms

from .constants import Interval, Triad
from .models import Chord, ChordType, ChordVoicing, Pitch, Relation, Scale


class ChordTypeForm(forms.ModelForm):
    class Meta:
        model = ChordType
        fields = ("name", "base", "seventh", "extensions")
        widgets = {"base": forms.Select(choices=Triad.choices)}
        widgets = {"seventh": forms.Select(choices=Interval.choices)}
        widgets = {"extensions": forms.SelectMultiple(choices=Interval.choices)}


@admin.register(ChordType)
class ChordTypeAdmin(admin.ModelAdmin):
    form = ChordTypeForm


@admin.register(Chord)
class ChordAdmin(admin.ModelAdmin):
    list_display = ("root", "chord_type")


admin.site.register(Pitch)
admin.site.register(Scale)


class ChordVoicingForm(forms.ModelForm):
    class Meta:
        model = ChordVoicing
        fields = ("chord", "pitches")

    def clean_pitches(self):
        chord = self.cleaned_data.get("chord")
        pitches = self.cleaned_data.get("pitches")

        missing_notes = [
            note.name for note in chord.notes
            if note not in pitches.values_list("note", flat=True)
        ]
        if missing_notes:
            raise ValidationError(
                _(
                    "Each note in %(chord)s must have a "
                    "corresponding pitch in the chord voicing. "
                    "Missing notes: %(notes)s"
                ),
                params={
                    "chord": chord,
                    "notes": missing_notes,
                },
            )

        invalid_pitches = [
            str(pitch) for pitch in pitches
            if pitch.note not in chord.notes
        ]
        if invalid_pitches:
            raise ValidationError(
                _(
                    "Invalid pitches: %(value)s. "
                    "Each pitch must correspond to a note in %(chord)s (%(notes)s)"
                ),
                params={
                    "value": str(invalid_pitches),
                    "chord": str(chord),
                    "notes": ", ".join([note.name for note in chord.notes]),
                },
            )
        return pitches


@admin.register(ChordVoicing)
class ChordVoicingAdmin(admin.ModelAdmin):
    form = ChordVoicingForm


class RelationForm(forms.ModelForm):
    class Meta:
        model = Relation
        fields = ("name", "transposition", "chord_type_a", "chord_type_b")
        widgets = {"transposition": forms.Select(choices=Interval.choices)}


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    form = RelationForm
