from rest_framework import generics
from rest_framework.response import Response

from chords.models import Chord, ChordType
from chords.serializers import ChordSerializer, ChordTypeSerializer


class ChordView(generics.ListAPIView):
    def get_queryset(self):
        return Chord.objects

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ChordSerializer(queryset, many=True)
        return Response(serializer.data)


class ChordTypeView(generics.ListAPIView):
    def get_queryset(self):
        return ChordType.objects

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ChordTypeSerializer(queryset, many=True)
        return Response(serializer.data)
