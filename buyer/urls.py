"""
Urls module for Buyer app.
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from buyer.views.buyer_views import (
    BuyerRetrieveAPIView,
    RegistrationAPIView,
)
from buyer.views.offer_views import OfferAPIView

router = SimpleRouter()
router.register("buyers", BuyerRetrieveAPIView)
router.register("offers", OfferAPIView)

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
