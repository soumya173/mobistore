import flask
from flask import request, jsonify
from flask_cors import CORS
import random
import string
import time

import dbhandler

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

"""
    Provides list of all the users configured in db
    Params:
        -
    Returns:
        - 200 with List Obj with all details of user
        - 200 with empty list if none found
"""
@app.route('/user/list', methods=['GET'])
def list_all_user():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    # Fetch all users
    query = 'SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users;'
    output = handler.fetch(query)
    return jsonify(output), 200

"""
    Provides user details for provided userid
    Params:
        - userid in URL
    Returns:
        - 200 with Obj with all details of user
        - 404 with empty list if none found
"""
@app.route('/user', methods=['GET'])
def get_user_by_id():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    userid = request.args.get('userid', type=int)
    handler = dbhandler.Dbhandler()
    query = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `userid`={}".format(userid)
    output = handler.fetch(query)

    if len(output) == 1:
        return jsonify(output[0]), 200
    else:
        return jsonify([]), 404

"""
    Add a new user with all the details provided
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with all details the newly created user
        - 400 with failure message
"""
@app.route('/user/add', methods=['POST'])
def add_new_user():
    if request.method not in ['POST']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate duplicate user before create
    # Create user
    query = "INSERT INTO users (`password`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified`) VALUES('{}', '{}', '{}', '{}', '{}', '{}', now(), now())".format(
                    content['password'],
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'])
    res = handler.execute(query)
    if res:
        # Verify the user got created
        getquery = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `firstname`='{}' AND `lastname`='{}' AND `email`='{}' AND `mobile`='{}' AND `type`='{}'".format(
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to create user'}
            rescode = 400
    else:
        response = {'message': 'Failed to create user'}
        rescode = 400
    return jsonify(response), rescode

"""
    Modifies an existing user
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with the details of modified user
        - 400 with failure message
"""
@app.route('/user/modify', methods=['PUT'])
def modify_user():
    if request.method not in ['PUT']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate if user exists
    # Modify user
    query = "UPDATE users SET `password`, `firstname`='{}', `lastname`='{}', `email`='{}', `mobile`='{}', `type`='{}', `modified`=now() WHERE userid={}".format(
                    content['password'],
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'],
                    content['userid'])
    res = handler.execute(query)
    if res:
        # Verify that the user modified
        getquery = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `userid`='{}' AND `firstname`='{}' AND `lastname`='{}' AND `email`='{}' AND `mobile`='{}' AND `type`='{}'".format(
                    content['userid'],
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to modify user, multiple rows received'}
            rescode = 400
    else:
        response = {'message': 'Failed to modify user'}
        rescode = 400
    return jsonify(response), rescode

"""
    Deletes an existing user
    Params:
        - JSON obj with userid and type
    Returns:
        - 200 with success message
        - 400 with failure message
"""
@app.route('/user/delete', methods=['DELETE'])
def delete_user():
    if request.method not in ['DELETE']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # Validate if user exists
    # Delete user
    query = "DELETE FROM users WHERE `type`='{}' AND `userid`='{}'".format(
                    content['type'],
                    content['userid'])
    res = handler.execute(query)
    if res:
        # Verify that the user deleted
        getquery = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `type`='{}' AND `userid`='{}'".format(
                    content['type'],
                    content['userid'])
        output = handler.fetch(getquery)
        if len(output) == 0:
            response = output
            rescode = 200
        else:
            response = {'message': 'Mutilple user deleted'}
            rescode = 400
    else:
        response = {'message': 'Failed to delete user'}
        rescode = 400
    return jsonify(response), rescode

"""
    Populates users table with random data
    Params:
        -
    Returns:
        - 200 with success message
"""
@app.route('/user/populate', methods=['POST'])
def populate_db():
    if request.method not in ['POST']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()

    # Populating users table
    for i in range(20):
        password = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        fname = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        lname = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        email = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)]) + '@gmail.com'
        mobile = ''.join([random.choice(string.digits) for _ in range(10)])
        typ = 'admin'

        query = "INSERT INTO users (`password`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified`) VALUES('{}', '{}', '{}', '{}', '{}', '{}', now(), now())".format(password, fname, lname, email, mobile, typ)
        res = handler.execute(query)

    # Populating products table
    getquery = "SELECT `userid` FROM users LIMIT 1"
    output = handler.fetch(getquery)
    addedby = output[0]['userid']
    for i in range(20):
        name = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        typ = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)])
        price = ''.join([random.choice(string.digits) for _ in range(3)])
        description = ''.join([random.choice(string.ascii_lowercase) for _ in range(20)])
        instock = 1

        query = "INSERT INTO products (`name`, `type`, `price`, `description`, `instock`, `created`, `modified`, `addedby`) VALUES('{}', '{}', '{}', '{}', '{}', now(), now(), '{}')".format(name, typ, price, description, instock, addedby)
        res = handler.execute(query)

    # Populating offers table
    getquery = "SELECT `productid` FROM products LIMIT 1"
    output = handler.fetch(getquery)
    productid = output[0]['productid']
    for i in range(20):
        description = ''.join([random.choice(string.ascii_lowercase) for _ in range(20)])
        discount = ''.join([random.choice(string.digits) for _ in range(2)])

        query = "INSERT INTO offers (`productid`, `addedby`, `discount`, `description`, `from`, `to`) VALUES('{}', '{}', '{}', '{}', now(), now())".format(productid, addedby, discount, description)
        res = handler.execute(query)
    return jsonify({'message': 'DB populated'}), 200


# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response

# Lets run the app with all the configured URLs
app.run()