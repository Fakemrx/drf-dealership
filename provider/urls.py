"""
Urls module for provider app.
"""
from rest_framework.routers import SimpleRouter

from provider.views.provider_views import ProviderAPIView

router = SimpleRouter()
router.register("providers", ProviderAPIView)

urlpatterns = router.urls
