"""Car app testing module for models."""
import pytest
from django.test import Client


@pytest.mark.django_db
def test_non_existing_page():
    """
    Testing if the car retrieve/update/destroy page for Car model
    with an ID 999999 will raise 404 error.
    """
    c = Client()
    response = c.get("/api/cars/r-u-d/999999")
    assert response.status_code == 404, "Should be 404"
