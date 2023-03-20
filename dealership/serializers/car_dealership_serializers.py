"""Serializers module for CarDealership model."""
from rest_framework import serializers

from dealership.models import CarDealership


class CarDealershipSerializer(serializers.ModelSerializer):
    """Serializer for CarDealership model."""

    class Meta:
        model = CarDealership
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        cars = []
        dealer = CarDealership.objects.get(id=instance.id)
        if dealer.preferred_cars_list.all():
            for car in dealer.preferred_cars_list.all():
                cars.append(str(car))
        rep["preferred_cars_list"] = cars
        return rep
