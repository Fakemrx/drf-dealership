"""
Initial testing module.
"""
from django.test import Client

c = Client()


def test_existing_page():
    """
    Testing if initial page will respond. (The response code should be 200)
    """
    response = c.get("/api/")
    assert response.status_code == 200, "Should be 200"


def test_non_existing_page():
    """
    Testing if non-existing page will provide error 404. (The response code should be 404)
    """
    response = c.get("/non-existing-page/")
    assert response.status_code == 404, "Should be 404"


def test_page_redirect():
    """
    Testing if "/admin/" URL will redirect to login page. (The response code should be 302)
    """
    response = c.get("/admin/")
    assert response.status_code == 302, "Should be 302"
