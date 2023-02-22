"""Module of CRUD APIViews for Engine model."""
from rest_framework import generics

from car.models import Engine
from car.serializers.engine_serializers import EngineSerializer


class EngineListCreateView(generics.ListCreateAPIView):
    """APIView create and list-view operations for Car model."""

    queryset = Engine.objects.all()
    serializer_class = EngineSerializer


class EngineRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """APIView retrieve, update, delete operations for Car model."""

    queryset = Engine.objects.all()
    serializer_class = EngineSerializer
