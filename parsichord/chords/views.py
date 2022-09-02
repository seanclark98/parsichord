from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response

from chords.models import Chord, ChordType
from chords.serializers import ChordSerializer, ChordTypeSerializer


class ChordView(viewsets.ModelViewSet):
    queryset = Chord.objects.all()
    serializer_class = ChordSerializer

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class ChordTypeView(generics.ListAPIView):
    def get_queryset(self):
        return ChordType.objects

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ChordTypeSerializer(queryset, many=True)
        return Response(serializer.data)
