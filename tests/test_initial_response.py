from django.test import Client

c = Client()


def test_check_acceptable_response():
    '''
    Testing if initial page will response. (The response code should be 200)
    '''
    response = c.get('')
    assert response.status_code == 200, "Should be 200"
