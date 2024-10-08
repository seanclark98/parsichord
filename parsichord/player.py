import threading
from time import sleep
from typing import Generator

import scamp
from pyabc import ChordBracket, Tune

from parsichord.chords import Note, Pitch


class Player:
    def __init__(self, tune: Tune):
        self.session = scamp.Session().run_as_server()
        self.session.tempo = 360
        self.piano = self.session.new_part("piano")
        self.cello = self.session.new_part("cello")
        self.tune = tune
        self.playhead = 0
        self.chord: list | None = None
        self.stop_arpeggio = False
        self.speed = 0.12

        self.timesteps = self.parse_tune()

    def arpeggiate(self, event: threading.Event) -> Generator[Note, None, None]:
        if self.chord is None:
            raise AttributeError(
                "Instance attribute 'chord' must be set before calling this method."
            )

        n = len(self.chord) - 1
        i = 0
        while True:
            if event.is_set():
                break
            if (i // n) % 2 == 0:
                j = i % n
            else:
                j = n - (i % n)
            yield self.chord[j]
            i += 1

    def play_arpeggio(self, event: threading.Event) -> None:
        volume = 0.5

        for note in self.arpeggiate(event):
            self.piano.play_note(note.pitch.midi_value + 24, volume, 3, blocking=False)
            sleep(self.speed / 2)

    def play_chord(self, chord: list[Note]) -> None:
        volume = 0.5
        if chord is None:
            return

        self.cello.play_chord(
            [note.pitch.midi_value for note in chord], volume, 9, blocking=False
        )

    def parse_tune(self) -> list[tuple[Note | None, list[Note] | None]]:
        timesteps: list[tuple[Note | None, list[Note] | None]] = []

        in_chord = False
        for token in self.tune.tokens:
            if isinstance(token, ChordBracket) and token._text == "[":
                chord = []
                in_chord = True
                continue
            if isinstance(token, Pitch | Note) and in_chord:
                chord.append(token)
                continue
            if isinstance(token, ChordBracket) and token._text == "]":
                self.chord = chord
                in_chord = False
                continue

            if isinstance(token, Note) and not in_chord:
                timesteps.append((token, chord))
                if token.duration > 1:
                    timesteps.extend([(None, None)] * int(token.duration - 1))

        return timesteps

    def play_jig(self) -> None:
        for playhead, (token, chord) in enumerate(self.timesteps):
            match playhead % 3:
                case 0:
                    intensity = 1.0
                    stretch = 1.1
                case 1:
                    intensity = 0.5
                    stretch = 0.9
                case 2:
                    intensity = 0.7
                    stretch = 1.0

            if token is not None:
                self.piano.play_note(
                    token.pitch.midi_value, intensity, token.duration * stretch
                )
            if playhead % 6 == 0 and chord is not None:
                self.play_chord(chord)
            sleep(self.speed * stretch)
