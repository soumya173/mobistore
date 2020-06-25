import flask
from flask import request, jsonify
from flask_cors import CORS
import random
import string

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
    Provides list of all the products configured in db
    Params:
        -
    Returns:
        - 200 with List Obj with all details of products
        - 200 with empty list if none found
"""
@app.route('/product/list', methods=['GET'])
def list_all_product():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    # Fetch all users
    query = 'SELECT * FROM products;'
    output = handler.fetch(query)
    return jsonify(output), 200

"""
    Provides product details for provided productid
    Params:
        - productid in URL
    Returns:
        - 200 with Obj with all details of product
        - 404 with empty list if none found
"""
@app.route('/product', methods=['GET'])
def get_product_by_id():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    productid = request.args.get('productid', type=int)
    handler = dbhandler.Dbhandler()
    query = "SELECT * FROM products WHERE `productid`={}".format(productid)
    output = handler.fetch(query)

    if len(output) == 1:
        return jsonify(output[0]), 200
    else:
        return jsonify([]), 404

"""
    Add a new product with all the details provided
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with all details the newly created product
        - 400 with failure message
"""
@app.route('/product/add', methods=['POST'])
def add_new_product():
    if request.method not in ['POST']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate duplicate product before create
    # Create product
    query = "INSERT INTO products (`offerid`, `name`, `type`, `price`, `description`, `instock`, `created`, `modified`, `addedby`) VALUES('{}', '{}', '{}', '{}', '{}', '{}', now(), now(), '{}')".format(
                    content['offerid'],
                    content['name'],
                    content['type'],
                    content['price'],
                    content['description'],
                    content['instock'],
                    content['addedby'])
    res = handler.execute(query)
    if res:
        # Verify the product got created
        getquery = "SELECT * FROM products WHERE `name`='{}' AND `price`='{}' AND `description`='{}' AND `instock`='{}' AND `type`='{}' AND `addedby`='{}'".format(
                    content['name'],
                    content['price'],
                    content['description'],
                    content['instock'],
                    content['type'],
                    content['addedby'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to create product'}
            rescode = 400
    else:
        response = {'message': 'Failed to create product'}
        rescode = 400
    return jsonify(response), rescode

"""
    Modifies an existing product
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with the details of modified product
        - 400 with failure message
"""
@app.route('/product/modify', methods=['PUT'])
def modify_product():
    if request.method not in ['PUT']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate if product exists
    # Modify product
    query = "UPDATE products SET `offerid`={}, `name`='{}', `type`='{}', `price`='{}', `description`='{}', `instock`={}, `modified`=now(), `addedby`={} WHERE productid={}".format(
                    content['offerid'],
                    content['name'],
                    content['type'],
                    content['price'],
                    content['description'],
                    content['instock'],
                    content['addedby'],
                    content['productid'])
    res = handler.execute(query)
    if res:
        # Verify that the product modified
        getquery = "SELECT * FROM products WHERE `offerid`='{}' AND `name`='{}' AND `type`='{}' AND `price`='{}' AND `description`='{}' AND `instock`='{}' AND `addedby`='{}' AND `productid`={}".format(
                    content['offerid'],
                    content['name'],
                    content['type'],
                    content['price'],
                    content['description'],
                    content['instock'],
                    content['addedby'],
                    content['productid'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to modify product, multiple rows received'}
            rescode = 400
    else:
        response = {'message': 'Failed to modify product'}
        rescode = 400
    return jsonify(response), rescode

"""
    Deletes an existing product
    Params:
        - JSON obj with productid and type
    Returns:
        - 200 with success message
        - 400 with failure message
"""
@app.route('/product/delete', methods=['DELETE'])
def delete_product():
    if request.method not in ['DELETE']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # Validate if product exists
    # Delete product
    query = "DELETE FROM products WHERE `type`='{}' AND `productid`='{}'".format(
                    content['type'],
                    content['productid'])
    res = handler.execute(query)
    if res:
        # Verify that the product deleted
        getquery = "SELECT * FROM products WHERE `type`='{}' AND `productid`='{}'".format(
                    content['type'],
                    content['productid'])
        output = handler.fetch(getquery)
        if len(output) == 0:
            response = output
            rescode = 200
        else:
            response = {'message': 'Mutilple product deleted'}
            rescode = 400
    else:
        response = {'message': 'Failed to delete product'}
        rescode = 400
    return jsonify(response), rescode

"""
    Provides list of all the offers configured in db
    Params:
        -
    Returns:
        - 200 with List Obj with all details of offers
        - 200 with empty list if none found
"""
@app.route('/offer/list', methods=['GET'])
def list_all_offer():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    # Fetch all users
    query = 'SELECT * FROM offers;'
    output = handler.fetch(query)
    return jsonify(output), 200

"""
    Provides offer details for provided offerid
    Params:
        - offerid in URL
    Returns:
        - 200 with Obj with all details of offer
        - 404 with empty list if none found
"""
@app.route('/offer', methods=['GET'])
def get_offer_by_id():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    offerid = request.args.get('offerid', type=int)
    handler = dbhandler.Dbhandler()
    query = "SELECT * FROM offers WHERE `offerid`={}".format(offerid)
    output = handler.fetch(query)

    if len(output) == 1:
        return jsonify(output[0]), 200
    else:
        return jsonify([]), 404

"""
    Add a new offer with all the details provided
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with all details the newly created offer
        - 400 with failure message
"""
@app.route('/offer/add', methods=['POST'])
def add_new_offer():
    if request.method not in ['POST']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate duplicate offer before create
    # Create offer
    query = "INSERT INTO offers (`productid`, `addedby`, `discount`, `description`, `from`, `to`) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(
                    content['productid'],
                    content['addedby'],
                    content['discount'],
                    content['description'],
                    content['from'],
                    content['to'])
    res = handler.execute(query)
    if res:
        # Verify the offer got created
        getquery = "SELECT * FROM offers WHERE `productid`='{}' AND `addedby`='{}' AND `description`='{}' AND `discount`='{}' AND `from`='{}' AND `to`='{}'".format(
                    content['productid'],
                    content['addedby'],
                    content['description'],
                    content['discount'],
                    content['from'],
                    content['to'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to create offer'}
            rescode = 400
    else:
        response = {'message': 'Failed to create offer'}
        rescode = 400
    return jsonify(response), rescode

"""
    Modifies an existing offer
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with the details of modified offer
        - 400 with failure message
"""
@app.route('/offer/modify', methods=['PUT'])
def modify_offer():
    if request.method not in ['PUT']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate if offer exists
    # Modify offer
    query = "UPDATE offers SET `productid`={}, `addedby`='{}', `discount`='{}', `description`='{}', `from`='{}', `to`='{}' WHERE offerid={}".format(
                    content['productid'],
                    content['addedby'],
                    content['discount'],
                    content['description'],
                    content['from'],
                    content['to'],
                    content['offerid'])
    res = handler.execute(query)
    if res:
        # Verify that the offer modified
        getquery = "SELECT * FROM offers WHERE `productid`='{}' AND `addedby`='{}' AND `discount`='{}' AND `description`='{}' AND `from`='{}' AND `to`='{}' AND `offerid`={}".format(
                    content['productid'],
                    content['addedby'],
                    content['discount'],
                    content['description'],
                    content['from'],
                    content['to'],
                    content['offerid'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to modify offer, multiple rows received'}
            rescode = 400
    else:
        response = {'message': 'Failed to modify offer'}
        rescode = 400
    return jsonify(response), rescode

"""
    Deletes an existing offer
    Params:
        - JSON obj with offerid and type
    Returns:
        - 200 with success message
        - 400 with failure message
"""
@app.route('/offer/delete', methods=['DELETE'])
def delete_offer():
    if request.method not in ['DELETE']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # Validate if offer exists
    # Delete offer
    query = "DELETE FROM offers WHERE `offerid`='{}'".format(
                    content['offerid'])
    res = handler.execute(query)
    if res:
        # Verify that the offer deleted
        getquery = "SELECT * FROM offers WHERE `offerid`='{}'".format(
                    content['offerid'])
        output = handler.fetch(getquery)
        if len(output) == 0:
            response = output
            rescode = 200
        else:
            response = {'message': 'Mutilple offer deleted'}
            rescode = 400
    else:
        response = {'message': 'Failed to delete offer'}
        rescode = 400
    return jsonify(response), rescode

"""
    Provides list of all the images configured in db
    Params:
        -
    Returns:
        - 200 with List Obj with all details of images
        - 200 with empty list if none found
"""
@app.route('/image/list', methods=['GET'])
def list_all_image():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    # Fetch all users
    query = 'SELECT * FROM images;'
    output = handler.fetch(query)
    return jsonify(output), 200

"""
    Provides image details for provided imageid
    Params:
        - imageid in URL
    Returns:
        - 200 with Obj with all details of image
        - 404 with empty list if none found
"""
@app.route('/image', methods=['GET'])
def get_image_by_id():
    if request.method not in ['GET']:
        return jsonify({"message": "Method not allowed"}), 405
    imageid = request.args.get('imageid', type=int)
    handler = dbhandler.Dbhandler()
    query = "SELECT * FROM images WHERE `imageid`={}".format(imageid)
    output = handler.fetch(query)

    if len(output) == 1:
        return jsonify(output[0]), 200
    else:
        return jsonify([]), 404

"""
    Add a new image with all the details provided
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with all details the newly created image
        - 400 with failure message
"""
@app.route('/image/add', methods=['POST'])
def add_new_image():
    if request.method not in ['POST']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate duplicate image before create
    # Create image
    query = "INSERT INTO images (`productid`, `url`) VALUES('{}', '{}')".format(
                    content['productid'],
                    content['url'])
    res = handler.execute(query)
    if res:
        # Verify the image got created
        getquery = "SELECT * FROM images WHERE `productid`='{}' AND `url`='{}'".format(
                    content['productid'],
                    content['url'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to create image'}
            rescode = 400
    else:
        response = {'message': 'Failed to create image'}
        rescode = 400
    return jsonify(response), rescode

"""
    Modifies an existing image
    Params:
        - JSON obj with all data
    Returns:
        - 200 with List Obj with the details of modified image
        - 400 with failure message
"""
@app.route('/image/modify', methods=['PUT'])
def modify_image():
    if request.method not in ['PUT']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # TODO: Validate if image exists
    # Modify image
    query = "UPDATE images SET `productid`={}, `url`='{}' WHERE imageid={}".format(
                    content['productid'],
                    content['url'],
                    content['imageid'])
    res = handler.execute(query)
    if res:
        # Verify that the image modified
        getquery = "SELECT * FROM images WHERE `productid`='{}' AND `url`='{}'".format(
                    content['productid'],
                    content['url'])
        output = handler.fetch(getquery)
        if len(output) == 1:
            response = output[0]
            rescode = 200
        else:
            response = {'message': 'Failed to modify image, multiple rows received'}
            rescode = 400
    else:
        response = {'message': 'Failed to modify image'}
        rescode = 400
    return jsonify(response), rescode

"""
    Deletes an existing image
    Params:
        - JSON obj with imageid and type
    Returns:
        - 200 with success message
        - 400 with failure message
"""
@app.route('/image/delete', methods=['DELETE'])
def delete_image():
    if request.method not in ['DELETE']:
        return jsonify({"message": "Method not allowed"}), 405
    handler = dbhandler.Dbhandler()
    content = request.json
    # Validate if image exists
    # Delete image
    query = "DELETE FROM images WHERE `imageid`='{}'".format(
                    content['imageid'])
    res = handler.execute(query)
    if res:
        # Verify that the image deleted
        getquery = "SELECT * FROM images WHERE `imageid`='{}'".format(
                    content['imageid'])
        output = handler.fetch(getquery)
        if len(output) == 0:
            response = output
            rescode = 200
        else:
            response = {'message': 'Mutilple image deleted'}
            rescode = 400
    else:
        response = {'message': 'Failed to delete image'}
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

if __name__ == '__main__':
    # Lets run the app with all the configured URLs
    app.run()