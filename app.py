from flask import Flask, jsonify
#from flasgger import Swagger
import s3
import os

app = Flask(__name__)
#swagger = Swagger(app)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

s3_client = s3.get_s3_client(app.config["S3_URL"], app.config["S3_KEY"], app.config["S3_SECRET"])

@app.route('/items/{id}', methods=["GET"])
def get_item_by_id(id):
    """
    Returns Item Object by ID
    ```
    parameters:
      - name: id
        in: path
        type: int
        required: true
    ```"""

    return """
        {
            'id': 1234,
            'name': 'Original Wavy Potato Chips',
            'upc': 0028400043809,
            'price': 4.20,
            'weight_mean': 28,
            'weight_std': 1,
            'color': 'red',
            'shape': 'chip_bag',
            'available': True,
            'item_thumb': '',
            'item_img': ''
        }"""
    
@app.route('/users/{id}', methods=["GET"])
def get_user_by_id(id):
    return """
        {
            'id': 1234,
            'rit_id': 12345678,
            'csh_id': 'jeffm',
            'name': 'Jeff Mahoney'
            'confidence': 0.98
        }"""

if __name__ == "__main__":
    app.run()