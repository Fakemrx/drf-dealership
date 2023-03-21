"""Adding Provider model in admin tool."""
from django.contrib import admin
from provider.models import (
    Provider,
    CarsInProviderStock,
    ProviderDiscounts,
    ProviderPersonalDiscounts,
)

admin.site.register(Provider)
admin.site.register(CarsInProviderStock)
admin.site.register(ProviderDiscounts)
admin.site.register(ProviderPersonalDiscounts)
