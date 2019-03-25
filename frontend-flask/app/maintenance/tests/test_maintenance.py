def test_200(client):
    """Provided token enables access to maintenance section"""

    response = client.get('/maintenance/?token=abc')
    assert 200 == response.status_code

def test_401(client):
    """No access without valid token"""

    response = client.get('/maintenance/')
    assert 401 == response.status_code