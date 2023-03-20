"""Adding CarDealership model in admin tool."""
from django.contrib import admin
from dealership.models import CarDealership, CarsInDealershipStock

admin.site.register(CarDealership)
admin.site.register(CarsInDealershipStock)
