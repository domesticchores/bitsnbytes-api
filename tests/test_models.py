import json
from api.models.item import Item

def test_item_tojson():
    temp_item = Item(id=1234, name="Original Wavy Potato Chips", upc='028400043809', price=4.20,
            weight_mean=28.0, weight_std=1.0, color="red", shape="chip_bag",
            available=True)
    
    correct = json.dumps({
            "id": 1234,
            "name": "Original Wavy Potato Chips",
            "upc": '028400043809',
            "price": 4.20,
            "weight_mean": 28.0,
            "weight_std": 1.0,
            "color": "red",
            "shape": "chip_bag",
            "available": True,
            "item_thumb": '',
            "item_img": ''
        })
    
    assert temp_item.to_json() == correct