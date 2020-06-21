import flask
from flask import request, jsonify
import random
import string
import time

import dbhandler

app = flask.Flask(__name__)
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
    handler = dbhandler.Dbhandler()
    query = 'SELECT * FROM users;'
    output = handler.fetch(query)
    return jsonify(output), 200

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
    handler = dbhandler.Dbhandler()
    content = request.json
    query = "INSERT INTO users (`firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified`) VALUES('{}', '{}', '{}', '{}', '{}', now(), now())".format(
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'])
    res = handler.execute(query)
    if res:
        # Verify the user got created
        getquery = "SELECT * FROM users WHERE `firstname`='{}' AND `lastname`='{}' AND `email`='{}' AND `mobile`='{}' AND `type`='{}'".format(
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output
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
    handler = dbhandler.Dbhandler()
    content = request.json
    query = "UPDATE users SET `firstname`='{}', `lastname`='{}', `email`='{}', `mobile`='{}', `type`='{}', `modified`=now() WHERE userid={}".format(
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'],
                    content['userid'])
    res = handler.execute(query)
    if res:
        # Verify that the user modified
        getquery = "SELECT * FROM users WHERE `firstname`='{}' AND `lastname`='{}' AND `email`='{}' AND `mobile`='{}' AND `type`='{}'".format(
                    content['firstname'],
                    content['lastname'],
                    content['email'],
                    content['mobile'],
                    content['type'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output
            rescode = 200
        else:
            response = {'message': 'Failed to modify user'}
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
    handler = dbhandler.Dbhandler()
    content = request.json
    query = "DELETE FROM users WHERE `type`='{}' AND `userid`='{}'".format(
                    content['type'],
                    content['userid'])
    res = handler.execute(query)
    if res:
        # Verify that the user deleted
        getquery = "SELECT * FROM users WHERE `type`='{}' AND `userid`='{}'".format(
                    content['type'],
                    content['userid'])
        output = handler.fetch(getquery)
        if len(output) == 0:
            response = {'message': 'User deleted successfully'}
            rescode = 200
        else:
            response = {'message': 'Failed to delete user'}
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
@app.route('/user/populate', methods=['GET'])
def populate_db():
    handler = dbhandler.Dbhandler()
    for i in range(20):
        fname = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        lname = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        email = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)]) + '@gmail.com'
        mobile = ''.join([random.choice(string.digits) for _ in range(10)])
        typ = 'admin'

        query = "INSERT INTO users (`firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified`) VALUES('{}', '{}', '{}', '{}', '{}', now(), now())".format(fname, lname, email, mobile, typ)
        res = handler.execute(query)
    return jsonify({'message': 'DB populated'}), 200

# Lets run the app with all the configured URLs
app.run()