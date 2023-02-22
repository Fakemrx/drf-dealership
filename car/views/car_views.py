"""Module of CRUD APIViews for Car model."""
from rest_framework import generics

from car.models import Car
from car.serializers.car_serializers import CarSerializer


class CarListCreateView(generics.ListCreateAPIView):
    """APIView create and list-view operations for Car model."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """APIView retrieve, update, delete operations for Car model."""

    queryset = Car.objects.all()
    serializer_class = CarSerializer
