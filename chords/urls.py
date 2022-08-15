from django.urls import path

from chords.views import ChordView, ChordTypeView

urlpatterns = [
    path("chords/", ChordView.as_view()),
    path("chord_type/", ChordTypeView.as_view()),
]
