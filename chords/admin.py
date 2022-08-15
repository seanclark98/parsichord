from django.contrib import admin
from django import forms

from .constants import Interval, Triad
from .models import Chord, ChordType, ChordVoicing, Pitch, Relation, Scale


class ChordTypeForm(forms.ModelForm):
    class Meta:
        model = ChordType
        # fields = ("name", "intervals")
        # widgets = {"intervals": forms.SelectMultiple(choices=Interval.choices)}
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

    def update_related_chords(self, request, queryset):
        for chord in queryset:
            chord.get_related_chords()

    actions = [update_related_chords]


admin.site.register(Pitch)
admin.site.register(Scale)


class ChordVoicingForm(forms.ModelForm):
    class Meta:
        model = ChordVoicing
        fields = ("chord", "pitches")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pitches"].queryset = Pitch.objects.filter(
            note__in=self.instance.chord.values_list("notes", flat=True)
        )


@admin.register(ChordVoicing)
class ChordVoicingAdmin(admin.ModelAdmin):
    form = ChordVoicingForm


class RelationForm(forms.ModelForm):
    class Meta:
        model = Relation
        fields = ("name", "transposition", "chord_type_i", "chord_type_j")
        widgets = {"transposition": forms.Select(choices=Interval.choices)}


@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    form = RelationForm
