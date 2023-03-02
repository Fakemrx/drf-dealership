"""
Urls module for Buyer app.
"""
from rest_framework.routers import SimpleRouter

from buyer.views.buyer_views import BuyerAPIView

router = SimpleRouter()
router.register("buyers", BuyerAPIView)

urlpatterns = router.urls
