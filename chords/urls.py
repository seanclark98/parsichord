from django.urls import path

from chords.views import ChordView, ChordTypeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'chords', ChordView, basename='chords')

urlpatterns = [
    # path("chords/", ChordView.as_view()),
    path("chord_type/", ChordTypeView.as_view()),
]
urlpatterns += router.urls
