def test_hello_world(client):
    """Hello world message on root access."""

    rv = client.get('/')
    assert b'Hello, World!' in rv.data