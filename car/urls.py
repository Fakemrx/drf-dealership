"""
Urls module for Car app.
"""
from django.urls import path
from car.views.car_views import CarListCreateView, CarRetrieveUpdateDeleteView
from car.views.engine_views import EngineListCreateView, EngineRetrieveUpdateDeleteView

urlpatterns = [
    path("", CarListCreateView.as_view(), name="list-create"),
    path(
        "<int:pk>/",
        CarRetrieveUpdateDeleteView.as_view(),
        name="retrieve-update-delete",
    ),
    path(
        "engines/",
        EngineListCreateView.as_view(),
        name="engine-list-create",
    ),
    path(
        "engines/<int:pk>/",
        EngineRetrieveUpdateDeleteView.as_view(),
        name="engine-retrieve-update-delete",
    ),
]
