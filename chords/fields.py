from typing import List

from multiselectfield import MultiSelectField

from django import forms
from django.db import models


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


def parse_intervals(intervals: list) -> List[Interval]:
    intervals = intervals.split(",")
    return [Interval(int(ivl)) for ivl in intervals]


class IntervalsField(MultiSelectField):
    def from_db_value(self, value, expression, connection) -> List[Interval]:
        if value is None:
            return value
        return parse_intervals(value)
