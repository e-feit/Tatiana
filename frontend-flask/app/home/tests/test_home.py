def test_hello_world(client):
    """Hello world message on root access."""

    response = client.get('/')
    assert b'Hello, World!' in response.data
    assert 200 == response.status_code

def test_styles(client):
    """Styles are rendered in html"""

    response = client.get('/')
    assert b'<link rel="stylesheet" href="/static/styles/style.css">' in response.data