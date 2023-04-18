"""
Urls module for Dealership app.
"""
from rest_framework.routers import SimpleRouter

from dealership.views.car_dealership_views import (
    CarDealershipAPIView,
    CarsInStockAPIView,
)

router = SimpleRouter()
router.register("dealerships", CarDealershipAPIView)
router.register("cars-in-stock", CarsInStockAPIView)

urlpatterns = router.urls
