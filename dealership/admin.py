"""Adding CarDealership model in admin tool."""
from django.contrib import admin
from dealership.models import CarDealership

admin.site.register(CarDealership)
