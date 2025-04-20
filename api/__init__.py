import datetime
from flask import Flask, jsonify, request, abort, Response
import os
import logging
import json
import api.util
import api.s3
from functools import wraps
from api.models.model import NFC, User
from api.models.item import Item, NutritionFact
from api.models.shelf import Interaction, Vision, Weight
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import json
from flask_cors import CORS, cross_origin
#from flasgger import Swagger

#swagger = Swagger(app)

app = Flask(__name__)
# set CORS options
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
    
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

print("WEBSITE: ", app.config["BNB_WEBSITE"])

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
            if request.headers["Authorization"] == f'{app.config["WEB_KEY"]}':
                print("Authorized with WEB credential")
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

# Items
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
            new_item = Item(request.get_json())
            db.session.add(new_item)
            db.session.commit()
            return str(new_item.id)
        except ValueError as value_err:
            return str(value_err), 400

"""
Get Item by ID
"""
@app.route('/items/<id>', methods=["GET", "PUT"])
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
        for field, value in request.form_data.items():
            if hasattr(item, field) and getattr(item, field) != value:
                setattr(item, field, value)
        db.session.commit()
    else:
        return json.dumps(item.as_dict())
    
"""
Deletes item object with given ID
"""
@app.route('/items/<id>', methods=["DELETE"])
@auth
def delete_item(id):
    item = db.get_or_404(Item, id)
    db.session.delete(item)
    db.session.commit()

    return ""

# Users
########################

"""
Get all users
"""
@app.route('/users/', methods=["GET"])
@auth
def get_all_users():
    """
    Returns all users as a json obj
    """
    print("GET Recieved")
    query = db.session.query(User)
    users = query.all()

    return [user.as_dict() for user in users]

"""
Create a User
"""
@app.route('/users/', methods=["POST"])
@auth
def add_user(nfc_data = None):
    """
    Creates a new user and returns its id
    """
    print("POST Recieved")
    try:
        if(not nfc_data):
            print("creating user from request")
            # json_data = json.loads(request.get_json(force=True))
            form_data = request.args.to_dict()
            print("DATA: ", request.form)
        else:
            print("creating user from nfc data")
            form_data = nfc_data
        new_user = User(form_data)
        print(f"DATA: {form_data}")
        db.session.add(new_user)
        db.session.commit()
        print(f"POST SUCCESS: UID {new_user.id}")
        return str(new_user.id)
    except ValueError as value_err:
        print(f"VALUE ERROR: {value_err}")
        return str(value_err), 400

"""
Get User by Token
"""
@app.route('/token/<token>', methods=["GET"])
@auth
def get_user_by_token(token):
    query = db.session.query(User).filter(User.token == token)
    if query.count() == 0:
        abort(404)

    user = query.one()

    return json.dumps(user.as_dict())

"""
Get User by ID
"""
@app.route('/users/<int:id>', methods=["GET", "PUT"])
@auth
def get_user_by_id(id):
    """
    Returns User Object by ID
    ```
    parameters:
    - name: id
        in: path
        type: int
        required: true
    ```
    """

    user = db.get_or_404(User, id)

    if request.method == "PUT":    
        for field, value in request.form_data.users():
            if hasattr(user, field) and getattr(user, field) != value:
                setattr(user, field, value)
        db.session.commit()
    else:
        return json.dumps(user.as_dict())
    
"""
Deletes user object with given ID
"""
@app.route('/users/<id>', methods=["DELETE"])
@auth
def delete_user(id):
    user = db.get_or_404(User, id)
    db.session.delete(user)
    db.session.commit()

    return id

# NFC
########################

"""
Gets NFC data
"""
@app.route('/nfc/', methods=["GET"])
@auth
def get_all_nfc_data():
    query = db.session.query(NFC)
    nfcs = query.all()

    return [nfc.as_dict() for nfc in nfcs]

"""
Adds NFC data
"""
@app.route('/nfc/', methods=["POST"])
@cross_origin(origins=[app.config["BNB_WEBSITE"]])
@auth
def add_nfc_data():
    try:
        data = request.args.to_dict()
        print(f"DATA: {data}")
        # first, check if there is already a user with the associated phone or email:
        user = db.session.query(User).filter(User.email == data["email"]).first()
        # if no user, then create one using the data given.
        userID = -1
        if (user == None):
             print("NO USER FOUND WITH EMAIL OR PHONE. CREATING.")
             data["balance"] = 10.00 # change this for amount to give each new user
             data["thumb_img"] = ''
             newID = add_user(nfc_data=data)
             userID = int(newID)
        else:
            print(f"USER DATA: {user.as_dict()}")
            userID = user.id
        print("USER ID: ", userID)
        
        nfc_data = {
            "id":data["nfc-token"],
            "assigned_user":userID,
            "type":"MIFARE"
        }
        
        nfc = NFC(nfc_data)       
        db.session.add(nfc)
        db.session.commit()
        print(f"POST SUCCESS")
        return nfc.as_dict(), 200
    except ValueError as value_err:
        print(f"VALUE ERROR: {value_err}")
        return str(value_err), "400 VALUE ERROR"
    except IntegrityError as int_err:
        print(f"INTEGRITY ERROR, SOMETHING ALREADY EXISTS: {int_err}")
        return str(int_err), "400 NFC ID ALREADY EXISTS"

"""
Get NFC by ID
"""
@app.route('/nfc/<id>', methods=["GET"])
@auth
def get_nfc_by_id(id):
    """
    Returns NFC Object by ID
    ```
    parameters:
    - name: id
        in: path
        type: int
        required: true
    ```
    """

    nfc = db.get_or_404(NFC, id)
    return nfc.as_dict(), 200

# Shelf Data
########################

# Interactions
########################
"""
Adds interactions to the database
"""
@app.route('/add_interactions', methods=["POST"])
@auth
def add_interactions():
    """
    Adds multiple interactions, from json body
    """
    print("POST Recieved")
    try:
        print("creating interactions from json")
        json_data = request.get_json(force=True)
        print("DATA: ", json_data)
        return_arr = list()
        for inter_json in json_data:
            interaction = Interaction(inter_json)
            db.session.add(interaction)
            db.session.commit()
            return_arr.append(str(interaction.time))
        return f"{len(return_arr)}", 200
    except ValueError as value_err:
        print(f"VALUE ERROR: {value_err}")
        return str(value_err), 400

# Vision
########################
"""
Adds vison data to the database
"""
@app.route('/add_visions', methods=["POST"])
@auth
def add_visions():
    """
    Adds multiple vision entries, from json body
    """
    print("POST Recieved")
    try:
        print("creating vision entries from json")
        json_data = request.get_json(force=True)
        print("DATA: ", json_data)
        return_arr = list()
        for inter_json in json_data:
            vision = Vision(inter_json)
            db.session.add(vision)
            db.session.commit()
            return_arr.append(str(vision.time))
        return f"{len(return_arr)}", 200
    except ValueError as value_err:
        print(f"VALUE ERROR: {value_err}")
        return str(value_err), 400

# Weight
########################
"""
Adds weight entries to the database
"""
@app.route('/add_weights', methods=["POST"])
@auth
def add_weights():
    """
    Adds multiple weight entries, from json body
    """
    print("POST Recieved")
    try:
        print("creating weights from json")
        json_data = request.get_json(force=True)
        print("DATA: ", json_data)
        return_arr = list()
        for inter_json in json_data:
            weight = Weight(inter_json)
            db.session.add(weight)
            db.session.commit()
            return_arr.append(str(weight.time))
        return f"{len(return_arr)}", 200
    except ValueError as value_err:
        print(f"VALUE ERROR: {value_err}")
        return str(value_err), 400

"""
Get vision and weight data based on timestamp
"""
@app.route('/training/<range>', methods=["GET"])
@auth
def get_training_data(range):
    start, end = range.split("~")

    try:
        datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
        datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        return "BAD PARAMETERS", 400
    
    query = db.session.query(Vision).filter(Vision.time.between(start, end))
    if query.count() == 0:
        return "NO RECORDS FOUND FOR VISION DATA", 404
    vision_data = [vision.as_string_dict() for vision in query.all()]

    query = db.session.query(Weight).filter(Weight.time.between(start, end))
    if query.count() == 0:
        return "NO RECORDS FOUND FOR WEIGHT DATA", 404
    weight_data = [weight.as_string_dict() for weight in query.all()]

    return json.dumps({"vision":vision_data,"weight":weight_data})
