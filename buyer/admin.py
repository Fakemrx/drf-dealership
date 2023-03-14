"""Adding Buyer and Offer models to admin tool."""
from django.contrib import admin

from buyer.models import Buyer, Offer

admin.site.register(Buyer)
admin.site.register(Offer)
