"""
Urls module for Dealership app.
"""
from rest_framework.routers import SimpleRouter

from dealership.views.car_dealership_views import CarDealershipAPIView

router = SimpleRouter()
router.register("dealerships", CarDealershipAPIView)

urlpatterns = router.urls
