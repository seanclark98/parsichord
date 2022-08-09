from rest_framework import generics
from rest_framework.response import Response

from chords.models import Chord
from chords.serializers import ChordSerializer


class ChordView(generics.ListAPIView):
    def get_queryset(self):
        return Chord.objects

    def list(self, request):
        qs = self.get_queryset()
        serializer = ChordSerializer(qs, many=True)
        return Response(serializer.data)
