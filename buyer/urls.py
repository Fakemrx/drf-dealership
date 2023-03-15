"""
Urls module for Buyer app.
"""
from rest_framework.routers import SimpleRouter

from buyer.views.buyer_views import BuyerRetrieveAPIView, UserAPIView
from buyer.views.offer_views import OfferAPIView

router = SimpleRouter()
router.register("buyers", BuyerRetrieveAPIView)
router.register("offers", OfferAPIView)
router.register("registration", UserAPIView)

urlpatterns = router.urls
