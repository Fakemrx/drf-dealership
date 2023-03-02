"""
Urls module for Car app.
"""
from rest_framework.routers import SimpleRouter

from car.views.car_views import CarAPIView
from car.views.engine_views import EngineAPIView

router = SimpleRouter()
router.register("cars", CarAPIView)
router.register("engines", EngineAPIView)

urlpatterns = router.urls
