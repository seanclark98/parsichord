from __future__ import annotations

from multiselectfield import MultiSelectField

from django import forms
from django.db import models

from .constants import Interval, Note


class IntervalFormField(forms.TypedChoiceField):
    def _coerce(self, value):
        try:
            return super()._coerce(int(value))
        except (TypeError, ValueError):
            return super()._coerce(None)


class IntervalField(models.IntegerField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return Interval(value)

    def to_python(self, value):
        if isinstance(value, Interval):
            return value

        if value is None:
            return value

        return Interval(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return value.value

    def formfield(self, **kwargs):
        defaults = {"choices_form_class": IntervalFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


def parse_intervals(intervals: str) -> list[Interval]:
    ivls = intervals.split(",")
    return [Interval(int(ivl)) for ivl in ivls]


class IntervalsField(MultiSelectField):
    def from_db_value(self, value, expression, connection) -> list[Interval]:
        if not value:
            return []
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
