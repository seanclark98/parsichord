from collections import deque
from typing import Iterable

from pyabc import ChordBracket, ChordSymbol, Note, Token, Tune

from parsichord.chords import Chord, ChordVoicing, Pitch
from parsichord.constants import PitchClass


class NotFound(Exception):
    pass


def nearest_parsimonious_chord_containing_pitch_class(
    chord: Chord, pitch_class: PitchClass
) -> Chord:
    queue: deque[Chord] = deque()
    seen = set()
    # implement bfs
    queue.append(chord)
    while queue:
        new_chord = queue.popleft()
        if pitch_class in new_chord.pitch_classes:
            return new_chord
        seen.add(new_chord)

        for parsimonious_chord in new_chord.parsimonious_chords():
            if parsimonious_chord not in seen:
                queue.append(parsimonious_chord)
    raise NotFound(f"No path from {chord} to Chord containing {pitch_class}")


def harmonize(tune: Tune, chord: Chord | None) -> Tune | None:
    previous_chord = None
    tokens = tune.tokens
    new_tokens = []

    for token in tokens:
        if chord is None:
            return None
        if not isinstance(token, Note):
            new_tokens.append(token)
            continue
        note = token
        pitch_class = note.pitch.pitch_class
        chord = nearest_parsimonious_chord_containing_pitch_class(chord, pitch_class)
        if chord != previous_chord:
            chord_symbol = ChordSymbol(
                line=token._line, char=token._char, text=f'"{chord}"'
            )
            new_tokens.extend([chord_symbol, note])
            previous_chord = chord
        else:
            new_tokens.append(note)

    abc = tune.compose_header_abc() + "".join(str(token) for token in new_tokens)
    return Tune(abc)


def nearest_parsimonious_chord_voicing_containing(
    chord_voicing: ChordVoicing, pitch: Pitch
) -> ChordVoicing:
    queue: deque[ChordVoicing] = deque()
    seen = set()
    # implement bfs
    queue.append(chord_voicing)
    while queue:
        new_chord_voicing = queue.popleft()
        if pitch.pitch_class in new_chord_voicing.chord.pitch_classes:
            return new_chord_voicing
        seen.add(new_chord_voicing.chord)

        for parsimonious_chord_voicing in new_chord_voicing.find_closest_voicings():
            if parsimonious_chord_voicing.chord not in seen:
                queue.append(parsimonious_chord_voicing)
    raise NotFound(f"No path from {chord_voicing} to ChordVoicing containing {pitch}")


def chord_voicing_tokens(token: Token, pitches: Iterable[Pitch]) -> list[Token]:
    chord_open_bracket = ChordBracket(line=token._line, char=token._char, text="[")
    chord_closed_bracket = ChordBracket(line=token._line, char=token._char, text="]")
    return [chord_open_bracket, *pitches, chord_closed_bracket]


def harmonize_with_voicings(tune: Tune, chord_voicing: ChordVoicing) -> ChordVoicing:
    previous_chord_voicing = None
    tokens = tune.tokens
    new_tokens = []

    for token in tokens:
        if chord_voicing is None:
            return None
        if not isinstance(token, Note):
            new_tokens.append(token)
            continue
        note = token
        pitch = note.pitch
        chord_voicing = nearest_parsimonious_chord_voicing_containing(
            chord_voicing, pitch
        )
        # chord = nearest_parsimonious_chord_containing_pitch_class(chord, pitch_class)
        if chord_voicing != previous_chord_voicing:
            chord_symbol = ChordSymbol(
                line=token._line, char=token._char, text=f'"{chord_voicing.chord}"'
            )
            pitches = sorted(chord_voicing.pitches, key=lambda p: p.abs_value)
            new_tokens.extend(
                [chord_symbol, *chord_voicing_tokens(token, pitches), note]
            )
            previous_chord_voicing = chord_voicing
        else:
            new_tokens.append(note)

    abc = tune.compose_header_abc() + "".join(str(token) for token in new_tokens)
    return Tune(abc=abc)
