"""
Urls module for Buyer app.
"""
from rest_framework.routers import SimpleRouter
from django.urls import path

from buyer.views.buyer_views import BuyerAPIView
from buyer.views.offer_views import OfferAPIView
from buyer.views.registration_view import register

router = SimpleRouter()
router.register("buyers", BuyerAPIView)
router.register("offers", OfferAPIView)

urlpatterns = [
    path("reg/", register, name="reg"),
]

urlpatterns += router.urls
