#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
import logging
from logging import Formatter, FileHandler

from utils import users, products
from forms import *

# Remove when testing is done
# Required to populate the db
from utils import dbhandler
import random, string

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
app.config.from_object('config')
# login = LoginManager(app)
# db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


# @app.route('/')
# def home():
#     return render_template('pages/placeholder.home.html')

# @app.route('/about')
# def about():
#     return render_template('pages/placeholder.about.html')


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session and session['loggedin'] == True:
        return redirect(url_for('logout'))
    if request.method == 'GET':
        form = LoginForm(request.form)
        return render_template('forms/login-form.html', form=form)
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.Users()
        user_details = user.authenticate_user(email, password)
        if user_details != False:
            session['loggedin'] = True
            session['userid'] = user_details['userid']
            session['email'] = user_details['email']
            return redirect(url_for('profile'))
        else:
            flash("Invalid Credentials")
            return render_template('forms/login-form.html', form=LoginForm(request.form))

@app.route('/admin/logout', methods=['GET'])
def logout():
    if 'loggedin' in session and session['loggedin'] == True:
        # Remove session data, this will log the user out
        session.pop('loggedin', None)
        session.pop('userid', None)
        session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/admin/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    userid = session['userid']
    user = users.Users()
    orig_user_details = user.get_user_by_id(userid)
    if request.method == 'GET':
        return render_template('forms/admin-profile-form.html', user=orig_user_details, form=AdminProfileForm(request.form))
    elif request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        user = users.Users()
        new_user_details = user.modify_user(password=password, firstname=firstname, lastname=lastname, email=email, mobile=mobile, type="admin", userid=userid)
        if new_user_details == False:
            flash("Failed to modify user details", "danger")
            return render_template('forms/admin-profile-form.html', user=orig_user_details, form=AdminProfileForm(request.form))
        else:
            flash("Profile modified", "success")
            return render_template('forms/admin-profile-form.html', user=new_user_details, form=AdminProfileForm(request.form))

@app.route('/admin/products', methods=['GET'])
def all_products():
    product = products.Products()
    all_products = product.get_all_product()
    return render_template('pages/admin-product-list.html', products=all_products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))

    if request.method == 'POST':
        offerid = request.form.get('offerid')
        name = request.form.get('name')
        type = request.form.get('type')
        price = request.form.get('price')
        description = request.form.get('description')
        instock = 1 if request.form.get('instock') == 'y' else 0
        addedby = request.form.get('addedby')

        product = products.Products()
        all_products = product.add_new_product(offerid=offerid, name=name, type=type, price=price, description=description, instock=instock, addedby=addedby)
        if all_products == False:
            flash("Failed to add new product. Please Try Again.", "danger")
            return render_template('forms/admin-product-add.html', form=AdminProductAdd(request.form))
        else:
            flash("Product added", "success")
    return render_template('forms/admin-product-add.html', form=AdminProductAdd(request.form))

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

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
