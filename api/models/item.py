import hashlib
import api.s3
import api.img
import json
from PIL import Image

class Item:
    def __init__(self, id, name, upc, price, weight_mean, weight_std, color, shape, available):
        self.id = id
        self.name = name
        self.upc = upc
        self.price = price
        self.weight_mean = weight_mean
        self.weight_std = weight_std
        self.color = color
        self.shape = shape
        self.available = available

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "upc": self.upc,
            "price": self.price,
            "weight_mean": self.weight_mean,
            "weight_std": self.weight_std,
            "color": self.color,
            "shape": self.shape,
            "available": self.available,
            "item_thumb": '',
            "item_img": ''
        })

    def add_image(file):
        """
        Processes image, adds to s3 and db
        """
        fullsizehash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)

        s3.upload_file(fullsizehash, file)

        with Image.open(file) as im:
            im = img.crop_center