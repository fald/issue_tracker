from tracker import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_basic_response(client):
    response = client.get('/test')
    assert response.data == b'Hello, Dev!'
