import pytest
import api

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_s3():
    return True

def test_getting_item_by_id():
    resp = client.get("/items/1234")
    
    assert '''{ \
            "id": 1234,
            "name": "Original Wavy Potato Chips",
            "upc": 28400043809,
            "price": 4.20, \
            "weight_mean": 28,
            "weight_std": 1,
            "color": "red",
            "shape": "chip_bag",
            "available": True,
            "item_thumb": "",
            "item_img": ""
        }''' in resp.data