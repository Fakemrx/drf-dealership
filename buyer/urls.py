"""
Urls module for Buyer app.
"""
from django.urls import path
from rest_framework.routers import SimpleRouter

from buyer.views.buyer_views import (
    BuyerRetrieveAPIView,
    RegistrationAPIView,
    AuthAPIView,
)
from buyer.views.offer_views import OfferAPIView

router = SimpleRouter()
router.register("buyers", BuyerRetrieveAPIView)
router.register("offers", OfferAPIView)

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("login/", AuthAPIView.as_view(), name="login"),
]

urlpatterns += router.urls
