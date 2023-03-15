"""Adding Provider model in admin tool."""
from django.contrib import admin
from provider.models import Provider, CarsInProviderStock

admin.site.register(Provider)
admin.site.register(CarsInProviderStock)
