from typing import List

from multiselectfield import MultiSelectField
from multiselectfield.forms.fields import MultiSelectFormField

# from django.core.validators import int_list_validator
from django import forms
from django.db import models
from django.utils.text import capfirst


class Note(models.IntegerChoices):
    C = 1
    Db = 2
    D = 3
    Eb = 4
    E = 5
    F = 6
    Gb = 7
    G = 8
    Ab = 9
    A = 10
    Bb = 11
    B = 12

    def __add__(self, interval: int):
        return Note((self.value + interval) % 12)


class NoteFormField(forms.TypedChoiceField):
    def _coerce(self, value):
        try:
            return super()._coerce(int(value))
        except TypeError:
            return super()._coerce(value)


class NoteField(models.IntegerField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Note(value)

    def to_python(self, value):
        if isinstance(value, Note):
            return value

        if value is None:
            return value

        return Note(value)

    def get_prep_value(self, value):
        return value.value

    def formfield(self, **kwargs):
        defaults = {"choices_form_class": NoteFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


# Interval = models.IntegerChoices("Intervals", "m2 M2 m3 M3 P4 dim5 P5 m6 M6 m7 M7")
class Interval(models.IntegerChoices):
    MINOR_SECOND = 1, "m2"
    MAJOR_SECOND = 2, "M2"
    MINOR_THIRD = 3, "m3"
    MAJOR_THIRD = 4, "M3"
    PERFECT_FOURTH = 5, "P4"
    DIMINISHED_FIFTH = 6, "dim5"
    PERFECT_FIFTH = 7, "P5"
    MINOR_SIXTH = 8, "m6"
    MAJOR_SIXTH = 9, "M6"
    MINOR_SEVENTH = 10, "m7"
    MAJOR_SEVENTH = 11, "M7"


def parse_intervals(value: str) -> List[Interval]:
    intervals = value
    # if isinstance(intervals, str):
    # intervals = intervals.split(",")

    return [Interval(int(ivl)) for ivl in intervals]


class IntervalsField(MultiSelectField):
    def from_db_value(self, value, expression, connection) -> List[Interval]:
        print("db value", value, type(value))
        if value is None:
            return value
        intervals = value.split(",")
        return parse_intervals(intervals)

    def to_python(self, value: str) -> List[Interval]:
        print("to_python value", value, type(value))
        if isinstance(value, list) and all(isinstance(ivl, Interval) for ivl in value):
            return value

        if value is None:
            return value

        return parse_intervals(value)

    def get_prep_value(self, value) -> List[int]:
        print("prep_value", value)
        return [ivl.value for ivl in value]

    def formfield(self, **kwargs):
        defaults = {
            "required": not self.blank,
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "choices": self.choices,
            "max_length": self.max_length,
            "max_choices": self.max_choices,
        }
        if self.has_default():
            defaults["initial"] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def validate(self, value, model_instance):
        super().validate([str(ivl.value) for ivl in value], model_instance)
