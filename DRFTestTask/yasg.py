"""Swagger UI config"""
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    info=openapi.Info(
        title="Dealership API",
        default_version="v1",
        description="API for buyers, dealerships and providers.",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
