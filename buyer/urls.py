"""
Urls module for Buyer app.
"""
from rest_framework.routers import SimpleRouter

from buyer.views.buyer_views import BuyerAPIView
from buyer.views.offer_views import OfferAPIView

router = SimpleRouter()
router.register("buyers", BuyerAPIView)
router.register("offers", OfferAPIView)

urlpatterns = router.urls
