import pytest
from api import app

@pytest.fixture()
def app():
    app.run(host=app.config['IP'], port=int(app.config['PORT']))
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_s3():
    assert True

def test_item_operations(client):
    resp = client.put("/items")
    assert resp.status == '200 OK'

    item_id = resp.data

    resp = client.post("/items/{0}".format(item_id))
    assert resp.status == '200 OK'

    resp = client.get("/items")
    assert resp.status == '200 OK'

    resp = client.get("/items/{0}".format(item_id))
    assert resp.status == '200 OK'

    resp = client.delete("/items/{0}".format(item_id))
    assert resp.status == '200 OK'