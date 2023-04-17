"""Adding CarDealership model in admin tool."""
from django.contrib import admin
from dealership.models import (
    CarDealership,
    CarsInDealershipStock,
    DealershipDiscounts,
    DealershipPersonalDiscounts,
    DealerSales,
)

admin.site.register(CarDealership)
admin.site.register(CarsInDealershipStock)
admin.site.register(DealershipDiscounts)
admin.site.register(DealershipPersonalDiscounts)
admin.site.register(DealerSales)
