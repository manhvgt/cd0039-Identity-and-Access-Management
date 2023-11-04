#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
setup_db(app)
CORS(app)

# Set up CORS. Allow '*' for origins.
CORS(app, resources={r"/*": {"origins": "*"}})

# Use the after_request decorator to set Access-Control-Allow
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all(app)


#----------------------------------------------------------------------------#
# ROUTES.
#----------------------------------------------------------------------------#
# index
@app.route('/')
def index():
    return jsonify({
        "success":True
    })

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#----------------------------------------------------------------------------#
# GET /drinks
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        # Query from DB
        drinks = Drink.query.all()
        if not drinks:
            abort(404)

        # Return drinks in JSON format
        short_drinks = [drink.short() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': short_drinks
        }), 200
    except Exception as error:
        abort(500)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#----------------------------------------------------------------------------#
# GET /drinks-detail
@app.route('/drinks-detail',methods=['GET'])
@requires_auth('get:drinks-detail')
def drinks_long(payload):
    try:
        # Query from DB
        drinks = Drink.query.all()
        if not drinks:
            abort(404)

        # Return drinks in JSON format
        long_drinks = [drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': long_drinks
        }), 200

    except Exception as error:
        abort(500)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
#----------------------------------------------------------------------------#
# POST /drinks
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    try:
        # get data and insert db
        form = request.get_json()
        drink = Drink(title=form['title'],recipe=json.dumps(form['recipe']))
        drink.insert()

    except Exception as error:
        abort(422)

    return jsonify({
        "success":True,
        "test":drink.long()
    }), 200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
#----------------------------------------------------------------------------#
# PATCH /drinks/<id>
@app.route("/drinks/<id>",methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(payload, id):
    try:
        # DB query
        drink = Drink.query.get(id)

        if not drink:
            abort(404)

        # processing
        form = request.get_json()
        if 'title' in form:
            drink.title = form['title']
        if 'recipe' in form:
            drink = json.dumps(form['recipe'])
        drink.update()

    except Exception as error:
        abort(422)

    return jsonify({
        "success": True,
        "drinks": [drink.long()],
    }), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
#----------------------------------------------------------------------------#
@app.route("/drinks/<id>",methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        # DB query
        matching_drink = Drink.query.get(id)

        if not matching_drink:
            abort(404)

        matching_drink.delete()

    except Exception as error:
        abort(422)

    return jsonify({
        "success": True,
        "delete": id
    }), 200


#----------------------------------------------------------------------------#
# Error Handling
'''
Example error handling for unprocessable entity
'''
# error handler for 422 (Unprocessable Entity)
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
# error handler for 404 (Not Found)
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

# error handler for 400 (Bad Request)
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

# error handler for 500 (Internal Server Error)
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500