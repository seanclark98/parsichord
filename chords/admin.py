from django.contrib import admin
from django import forms

from chords.models import Chord, ChordType, Interval, Pitch, Scale


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
