"""
Initial testing module.
"""
from django.test import Client
from rest_framework import status

c = Client()


def test_existing_page():
    """
    Testing if initial page will respond. (The response code should be 200)
    """
    response = c.get("/api/")
    assert response.status_code == status.HTTP_200_OK, "Should be 200"


def test_non_existing_page():
    """
    Testing if non-existing page will provide error 404. (The response code should be 404)
    """
    response = c.get("/non-existing-page/")
    assert response.status_code == status.HTTP_404_NOT_FOUND, "Should be 404"


def test_page_redirect():
    """
    Testing if "/admin/" URL will redirect to login page. (The response code should be 302)
    """
    response = c.get("/admin/")
    assert response.status_code == status.HTTP_302_FOUND, "Should be 302"
