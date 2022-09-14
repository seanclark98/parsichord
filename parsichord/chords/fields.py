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

    def get_prep_value(self, value: Interval | None) -> int | None:
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
    def from_db_value(self, value: str, expression, connection) -> list[Interval]:
        if not value:
            return []
        return parse_intervals(value)


def parse_notes(notes_str: str) -> set[Note]:
    if not notes_str:
        return set()
    notes = notes_str.split(",")
    return set(Note(int(note)) for note in notes)


class NotesField(models.Field):
    def from_db_value(self, value: str, expression, connection) -> set[Note]:
        if not value:
            return set()
        return parse_notes(value)

    def to_python(self, value: str) -> set[Note] | None:
        if isinstance(value, set) and all([isinstance(note, Note) for note in value]):
            return value

        if value is None:
            return value

        return parse_notes(value)

    def get_prep_value(self, value: list[Note]) -> str:
        return ','.join([str(note.value) for note in value])

    def get_internal_type(self) -> str:
        return 'CharField'


class NoteFormField(forms.TypedChoiceField):
    def _coerce(self, value):
        try:
            return super()._coerce(int(value))
        except TypeError:
            return super()._coerce(value)


class NoteField(models.IntegerField):
    def from_db_value(self, value, expression, connection) -> Note | None:
        if value is None:
            return value
        return Note(value)

    def to_python(self, value) -> Note | None:
        if isinstance(value, Note):
            return value

        if value is None:
            return value

        return Note(value)

    def get_prep_value(self, value) -> int:
        return value.value

    def formfield(self, **kwargs):
        defaults = {"choices_form_class": NoteFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)
