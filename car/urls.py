"""
Urls module for Car app.
"""
from django.urls import path
from car.views.car_views import CarListCreateView, CarRetrieveUpdateDeleteView
from car.views.engine_views import EngineListCreateView, EngineRetrieveUpdateDeleteView

urlpatterns = [
    path("list-create/", CarListCreateView.as_view(), name="list-create"),
    path(
        "r-u-d/<int:pk>",
        CarRetrieveUpdateDeleteView.as_view(),
        name="retrieve-update-delete",
    ),
    path(
        "engines/list-create/",
        EngineListCreateView.as_view(),
        name="engine-list-create",
    ),
    path(
        "engines/r-u-d/<int:pk>",
        EngineRetrieveUpdateDeleteView.as_view(),
        name="engine-retrieve-update-delete",
    ),
]
