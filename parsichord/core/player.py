import threading
from time import sleep
from typing import Generator

import scamp

from .tune import ChordVoicing, Note, Tune


class Player:
    def __init__(self, tune: Tune, melody: str = "harp", accompaniment: str = "cello"):
        self.session = scamp.Session().run_as_server()
        self.session.tempo = 360
        self.melody = self.session.new_part(melody)
        self.accompaniment = self.session.new_part(accompaniment)
        self.tune = tune
        self.playhead = 0
        self.chord: list | None = None
        self.stop_arpeggio = False
        self.speed = 0.12

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
            self.melody.play_note(note.pitch.midi_value + 24, volume, 3, blocking=False)
            sleep(self.speed / 2)

    def play_chord(self, chord: ChordVoicing) -> None:
        volume = 0.5
        self.accompaniment.play_chord(
            [pitch.midi_value for pitch in chord.pitches], volume, 10, blocking=False
        )

    def play_jig(
        self,
        play_melody: bool = True,
        play_chords: bool = True,
        speed: float | None = None,
        swing: float = 1,
        slip: bool = False,
    ) -> None:
        if speed is not None:
            self.speed = speed

        if slip:
            beats_per_bar = 3
        else:
            beats_per_bar = 2

        # last_chord = None
        for playhead, note in enumerate(self.tune.notes):
            match playhead % 3:
                case 0:
                    intensity = 1.0
                    stretch = (swing / (swing + 1)) * 2
                case 1:
                    intensity = 0.5
                    stretch = (1 / (swing + 1)) * 2
                case 2:
                    intensity = 0.7
                    stretch = 1.0

            if note is not None and play_melody:
                self.melody.play_note(
                    note.pitch.midi_value, intensity, note.duration * stretch
                )

            chord = self.tune.get_chord(playhead)
            if (
                playhead % (beats_per_bar * 3) == 0
                and chord is not None
                and play_chords
                # and chord != last_chord
            ):
                self.play_chord(chord)
                print(chord)
                # last_chord = chord
            sleep(self.speed * stretch)

    def play_reel(
        self,
        play_melody: bool = True,
        play_chords: bool = True,
        speed: float | None = None,
        swing: float = 1,
    ) -> None:
        if speed is not None:
            self.speed = speed

        beats_per_bar = 4

        # last_chord = None
        for playhead, note in enumerate(self.tune.notes):
            match playhead % 4:
                case 0:
                    intensity = 1.0
                    stretch = (swing / (swing + 1)) * 2
                case 1:
                    intensity = 0.7
                    stretch = (1 / (swing + 1)) * 2
                case 2:
                    intensity = 0.7
                    stretch = 1.0
                case 3:
                    intensity = 0.7
                    stretch = 1.0

            if note is not None and play_melody:
                self.melody.play_note(
                    note.pitch.midi_value, intensity, note.duration * stretch
                )

            chord = self.tune.get_chord(playhead)
            if (
                playhead % beats_per_bar == 0
                and chord is not None
                and play_chords
                # and chord != last_chord
            ):
                self.play_chord(chord)
                print(chord)
                # last_chord = chord
            sleep(self.speed * stretch)
