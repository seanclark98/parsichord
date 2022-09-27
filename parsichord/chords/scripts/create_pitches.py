from ..constants import Note
from ..models import Pitch


def create_pitches():
    pitch = Pitch.objects.create(note=Note.E, octave=2)

    pitches_in_an_octave = 12
    for i in range(4 * pitches_in_an_octave):
        pitch + i


if __name__ == "__main__":
    create_pitches()