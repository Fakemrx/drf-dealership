"""Registry of Provider model in admin tool."""
from django.contrib import admin
from provider.models import Provider

admin.site.register(Provider)
