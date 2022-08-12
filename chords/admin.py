from django.contrib import admin
from django import forms

from .models import Chord, ChordType, ChordVoicing, Interval, Pitch, Scale


class ChordTypeForm(forms.ModelForm):
    class Meta:
        model = ChordType
        fields = ("name", "intervals")
        widgets = {"intervals": forms.SelectMultiple(choices=Interval.choices)}


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pitches"].queryset = Pitch.objects.filter(
            note__in=self.instance.chord.values_list("notes", flat=True)
        )


@admin.register(ChordVoicing)
class ChordVoicingAdmin(admin.ModelAdmin):
    form = ChordVoicingForm
