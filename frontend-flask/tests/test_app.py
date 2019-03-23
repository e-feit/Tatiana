def test_hello_world(client):
    """Hello world message on root access."""

    response = client.get('/')
    assert b'Hello, World!' in response.data
    assert 200 == response.status_code