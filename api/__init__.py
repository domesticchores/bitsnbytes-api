from flask import Flask, request, abort
import os
import logging
import json
import api.util
import api.s3
from functools import wraps
from api.models.item import Item
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
from sqlalchemy.orm import Session
#from flasgger import Swagger

#swagger = Swagger(app)

app = Flask(__name__)
    
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
    app.config["DBUSER"],
    app.config["DBPWD"],
    app.config["DBHOST"],
    app.config["DBPORT"],
    app.config["DBNAME"],
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# Commit
#commit = check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').rstrip()

########################
#
# Helpers
#
########################

"""
Handle errors
"""
@app.errorhandler(404)
def page_not_found(e):
    resp = e.get_response()
    resp.data = json.dumps({
        'code': e.code,
        'name': e.name,
        'description': e.description
    })
    resp.content_type = 'application/json'
    return resp

"""
Auth required wrapper
"""
def auth(f):
    @wraps(f)
    def wrapped(**kwargs):
        if "Authorization" in request.headers:
            if request.headers["Authorization"] == f'{app.config["UI_KEY"]}':
                print("Authorized with UI credential")
                return f(**kwargs)
            if request.headers["Authorization"] == f'{app.config["AI_KEY"]}':
                print("Authorized with AI credential")
                return f(**kwargs)
            if request.headers["Authorization"] == f'{app.config["EXTRA_KEY"]}':
                print("Authorized with EXTRA credential")
                return f(**kwargs)
        return abort(403)
    return wrapped

########################
# 
# Routes
# 
########################

"""
Get all items
"""
@app.route('/items', methods=["GET", "POST"])
@auth
def get_all_items():
    """
    Returns all items as a json obj
    """
    
    if request.method == "GET":
        query = db.session.query(Item)
        items = query.all()

        return [item.as_dict() for item in items]
    
    else:
        try:
            print(request.get_json())
            new_item = Item(request.get_json())
            db.session.add(new_item)
            db.session.commit()
        except ValueError as value_err:
            return str(value_err), 400

"""
Get Item by ID
"""
@app.route('/items/<id>', methods=["GET", "POST"])
@auth
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

    item = db.get_or_404(Item, id)

    if request.method == "PUT":
        pass
    else:
        return str(item.as_dict())

"""
Edit item by ID
"""
@app.route('/items/<id>', methods=["POST"])
@auth
def edit_item(id):
    item = db.get_or_404(Item, id)

    print(item.id)

    return ""

    if(item_exists(id)):
        db.edit_item(id, request.form)
        return get_item_by_id(id)
    else:
        return flask.redirect('/404')

"""
Add item, return ID
"""
@app.route('/items', methods=["PUT"])
@auth
def add_item():

    item = Item()

    return '{}'.format(item.id)
    
"""
Deletes item object with given ID
"""
@app.route('/items/<id>', methods=["DELETE"])
@auth
def delete_item(id):

    return util.format_return_msg("Item {0} Deleted".format(id))

@app.route('/users/<id>', methods=["GET"])
@auth
def get_user_by_id(id):
    return """
        {
            'id': 1234,
            'rit_id': 12345678,
            'csh_id': 'jeffm',
            'name': 'Jeff Mahoney'
            'confidence': 0.98
        }"""
