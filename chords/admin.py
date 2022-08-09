from django.contrib import admin

from chords.models import Chord, Pitch, Scale

# Register your models here.
admin.site.register(Chord)
admin.site.register(Pitch)
admin.site.register(Scale)
