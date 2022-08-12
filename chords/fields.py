from typing import List

from multiselectfield import MultiSelectField

from django import forms
from django.db import models

from .constants import Interval, Note


def parse_intervals(intervals: list) -> List[Interval]:
    intervals = intervals.split(",")
    return [Interval(int(ivl)) for ivl in intervals]


class IntervalsField(MultiSelectField):
    def from_db_value(self, value, expression, connection) -> List[Interval]:
        if value is None:
            return value
        return parse_intervals(value)


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
