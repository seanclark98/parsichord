from collections import deque

from pyabc import ChordSymbol, Note, Tune

from parsichord.chords import Chord
from parsichord.constants import PitchClass


def nearest_parsimonious_chord_containing_pitch_class(
    chord: Chord, pitch_class: PitchClass
) -> Chord | None:
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
    return None


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
