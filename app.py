#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import logging
from logging import Formatter, FileHandler
import os

from utils import users, products, offers, images
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

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
@app.route('/')
def home():
    return render_template('pages/main-launch-page.html')

@app.route('/products')
def main_products():
    product = products.Products()
    all_products = product.get_all_product()
    return render_template('pages/main-products-list.html', products=all_products)

@app.route('/about')
def about():
    return render_template('layouts/developer-about.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session and session['loggedin'] == True:
        return redirect(url_for('logout'))
    if request.method == 'GET':
        form = LoginForm(request.form)
        return render_template('forms/login-form.html', form=form)
    elif request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
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
                flash("Invalid Credentials", "danger")
                return render_template('forms/login-form.html', form=form)
        else:
            flash("Invalid inputs provided", "danger")
            return render_template('forms/login-form.html', form=form)

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
        form = AdminProfileForm(request.form)
        if form.validate():
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            mobile = request.form.get('mobile')
            password = request.form.get('password')
            confirm = request.form.get('confirm')

            user = users.Users()
            new_user_details = user.modify_user(password=password, firstname=firstname, lastname=lastname, mobile=mobile, type="admin", userid=userid)
            if new_user_details == False:
                flash("Failed to modify user details", "danger")
                return render_template('forms/admin-profile-form.html', user=orig_user_details, form=form)
            else:
                flash("Profile modified", "success")
                return render_template('forms/admin-profile-form.html', user=new_user_details, form=form)
        else:
            flash("Invalid inputs provided", "danger")
            return render_template('forms/admin-profile-form.html', user=orig_user_details, form=form)

@app.route('/admin/users', methods=['GET'])
def all_users():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    user = users.Users()
    all_users = user.get_all_user()
    return render_template('pages/admin-user-list.html', users=all_users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
def add_user():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('forms/admin-user-add.html', form=AdminUserAdd(request.form))
    if request.method == 'POST':
        form = AdminUserAdd(request.form)
        if form.validate():
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            mobile = request.form.get('mobile')
            email = request.form.get('email')
            password = request.form.get('password')
            type = "admin"

            user = users.Users()
            new_user = user.add_new_user(password=password, firstname=firstname, lastname=lastname, email=email, mobile=mobile, type=type)
            if new_user == False:
                flash("Failed to add new User.", "danger")
                return render_template('forms/admin-user-add.html', form=form)
            else:
                flash("User added", "success")
                return render_template('forms/admin-user-add.html', form=form)
        else:
            flash("Invalid inputs provided", "danger")
            return render_template('forms/admin-user-add.html', form=form)

@app.route('/admin/users/modify', methods=['GET', 'POST'])
def modify_user():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    userid = request.args.get('id')
    user = users.Users()
    user_details = user.get_user_by_id(userid=userid)
    if request.method == 'GET':
        if user_details == False:
            flash("User Not Found")
            redirect(url_for('all_users'))
        return render_template('forms/admin-user-modify.html', users=user_details, form=AdminUserModify(request.form))
    if request.method == 'POST':
        form = AdminUserModify(request.form)
        if form.validate():
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            mobile = request.form.get('mobile')
            password = request.form.get('password')
            type = "admin"

            user = users.Users()
            modified_user = user.modify_user(password=password, firstname=firstname, lastname=lastname, mobile=mobile, type=type, userid=userid)
            if modified_user == False:
                flash("Failed to modify user", "danger")
                return render_template('forms/admin-user-modify.html', users=user_details, form=form)
            else:
                flash("User modified", "success")
                return render_template('forms/admin-user-modify.html', users=modified_user, form=form)
        else:
            flash("Invalid inputs provided", "danger")
            flash(form.errors, "danger")
            return render_template('forms/admin-user-modify.html', users=user_details, form=form)

@app.route('/admin/users/delete', methods=['GET'])
def delete_user():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    userid = request.args.get('id')
    user = users.Users()
    user_details = user.delete_user_by_id(userid=userid)
    if user_details == False:
        flash("Failed to delete user", "danger")
        return redirect(url_for('all_users'))
    else:
        flash("User deleted", "success")
        return redirect(url_for('all_users'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin/products', methods=['GET'])
def all_products():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    product = products.Products()
    all_products = product.get_all_product()
    return render_template('pages/admin-product-list.html', products=all_products)

def allowed_file(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('forms/admin-product-add.html', form=AdminProductAdd(request.form))
    if request.method == 'POST':
        form = AdminProductAdd(request.form)
        if form.validate():
            offerid = request.form.get('offerid')
            name = request.form.get('name')
            type = request.form.get('type')
            labels = request.form.get('labels') if request.form.get('labels') is not None else ""
            price = request.form.get('price')
            description = request.form.get('description')
            instock = 1 if request.form.get('instock') == 'on' else 0
            addedby = session['userid']

            product = products.Products()
            all_products = product.add_new_product(offerid=offerid, name=name, type=type, price=price, description=description, instock=instock, addedby=addedby, labels=labels)
            if all_products == False:
                flash("Failed to add new product", "danger")
                return render_template('forms/admin-product-add.html', form=form)
            else:
                if 'file' in request.files:
                    files = request.files.getlist('file')
                    for file in files:
                        if file.filename != '':
                            if file and allowed_file(file.filename):
                                filename = "{}_{}".format(all_products['productid'], secure_filename(file.filename))
                                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                                image = images.Images()
                                new_image = image.add_new_image(all_products['productid'], url_for('uploaded_file', filename=filename))
                                if new_image == False:
                                    flash("Failed update image url in db", "danger")
                            else:
                                flash("File type not supported", "danger")
                flash("Product added", "success")
                return render_template('forms/admin-product-add.html', form=form)
        else:
            flash("Invalid inputs provided", "danger")
            return render_template('forms/admin-product-add.html', form=form)

@app.route('/admin/products/modify', methods=['GET', 'POST'])
def modify_product():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))

    productid = request.args.get('id')
    product = products.Products()
    product_details = product.get_product_by_id(productid=productid)
    if request.method == 'GET':
        if product_details == False:
            flash("Product Not Found")
            redirect(url_for('all_products'))
        return render_template('forms/admin-product-modify.html', products=product_details, form=AdminProductAdd(request.form))
    if request.method == 'POST':
        form = AdminProductAdd(request.form)
        if form.validate():
            offerid = 0 if request.form.get('offerid') == 'None' else request.form.get('offerid')
            name = request.form.get('name')
            type = request.form.get('type')
            labels = request.form.get('labels') if request.form.get('labels') is not None else ""
            price = request.form.get('price')
            description = request.form.get('description')
            instock = 1 if request.form.get('instock') == 'on' else 0
            addedby = session['userid']
            productid = request.args.get('id')

            product = products.Products()
            modified_product = product.modify_product(offerid=offerid, name=name, type=type, price=price, description=description, instock=instock, addedby=addedby, labels=labels, productid=productid)
            if modified_product == False:
                flash("Failed to modify product", "danger")
                return render_template('forms/admin-product-modify.html', products=product_details, form=form)
            else:
                flash("Product modified", "success")
                return render_template('forms/admin-product-modify.html', products=modified_product, form=form)
        else:
            flash("Invalid inputs provided", "danger")
            return render_template('forms/admin-product-modify.html', products=product_details, form=form)

@app.route('/admin/products/delete', methods=['GET'])
def delete_product():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    productid = request.args.get('id')
    product = products.Products()
    product_details = product.delete_product_by_id(productid=productid)
    if product_details == False:
        flash("Failed to delete product", "danger")
        return redirect(url_for('all_products'))
    else:
        flash("Product deleted", "success")
        return redirect(url_for('all_products'))

@app.route('/admin/images', methods=['GET'])
def all_images():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    image = images.Images()
    all_images = image.get_all_image()
    return render_template('pages/admin-image-list.html', images=all_images)

@app.route('/admin/offers', methods=['GET'])
def all_offers():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    offer = offers.Offers()
    all_offers = offer.get_all_offer()
    return render_template('pages/admin-offer-list.html', offers=all_offers)

@app.route('/admin/offers/add', methods=['GET', 'POST'])
def add_offer():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('forms/admin-offer-add.html', form=AdminOfferAdd(request.form))
    elif request.method == 'POST':
        form = AdminOfferAdd(request.form)
        if form.validate():
            discount = request.form.get('discount')
            description = request.form.get('description')
            fromd = request.form.get('fromd')
            tod = request.form.get('tod')
            addedby = session['userid']

            offer = offers.Offers()
            new_offer = offer.add_new_offer(addedby=addedby, discount=discount, description=description, fromd=fromd, tod=tod)
            if new_offer == False:
                flash("Failed to add new offer", "danger")
                return render_template('forms/admin-offer-add.html', form=form)
            else:
                flash("Offer added", "success")
                return render_template('forms/admin-offer-add.html', form=form)
        else:
            flash("Invalid inputs provided", "danger")
            return render_template('forms/admin-offer-add.html', form=form)

@app.route('/admin/offers/modify', methods=['GET', 'POST'])
def modify_offer():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    offerid = request.args.get('id')
    offer = offers.Offers()
    offer_details = offer.get_offer_by_id(offerid=offerid)
    if request.method == 'GET':
        if offer_details == False:
            flash("Offer Not Found", "danger")
            redirect(url_for('all_offers'))
        return render_template('forms/admin-offer-modify.html', offers=offer_details, form=AdminOfferAdd(request.form))
    elif request.method == 'POST':
        form = AdminOfferAdd(request.form)
        if form.validate():
            discount = request.form.get('discount')
            description = request.form.get('description')
            fromd = request.form.get('fromd')
            tod = request.form.get('tod')
            addedby = session['userid']
            offerid = request.args.get('id')

            offer = offers.Offers()
            new_offer = offer.modify_offer(addedby=addedby, discount=discount, description=description, fromd=fromd, tod=tod, offerid=offerid)
            if new_offer == False:
                flash("Failed to modify new offer", "danger")
                return render_template('forms/admin-offer-modify.html', offers=offer_details, form=form)
            else:
                flash("Offer modified", "success")
                return render_template('forms/admin-offer-modify.html', offers=new_offer, form=form)
        else:
            flash("Invalid inputs provided", "danger")
            return render_template('forms/admin-offer-modify.html', offers=new_offer, form=form)

@app.route('/admin/offers/delete', methods=['GET'])
def delete_offer():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    offerid = request.args.get('id')
    offer = offers.Offers()
    offer_details = offer.delete_offer_by_id(offerid=offerid)
    if offer_details == False:
        flash("Failed to delete offer", "danger")
        return redirect(url_for('all_offers'))
    else:
        flash("Offer deleted", "success")
        return redirect(url_for('all_offers'))

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

    # Populating offers table
    getquery = "SELECT `userid` FROM users LIMIT 1"
    output = handler.fetch(getquery)
    addedby = output[0]['userid']
    for i in range(20):
        description = ''.join([random.choice(string.ascii_lowercase) for _ in range(20)])
        discount = ''.join([random.choice(string.digits) for _ in range(2)])

        query = "INSERT INTO offers (`addedby`, `discount`, `description`, `from`, `to`) VALUES('{}', '{}', '{}', now(), now())".format(addedby, discount, description)
        res = handler.execute(query)

    # Populating products table
    getquery = "SELECT `offerid` FROM offers LIMIT 1"
    output = handler.fetch(getquery)
    offerid = output[0]['offerid']
    for i in range(20):
        name = ''.join([random.choice(string.ascii_lowercase) for _ in range(10)])
        typ = ''.join([random.choice(string.ascii_lowercase) for _ in range(5)])
        price = ''.join([random.choice(string.digits) for _ in range(3)])
        description = ''.join([random.choice(string.ascii_lowercase) for _ in range(20)])
        instock = 1

        query = "INSERT INTO products (`name`, `type`, `price`, `description`, `instock`, `created`, `modified`, `addedby`, `offerid`) VALUES('{}', '{}', '{}', '{}', '{}', now(), now(), '{}', '{}')".format(name, typ, price, description, instock, addedby, offerid)
        res = handler.execute(query)

    return jsonify({'message': 'DB populated'}), 200

# Error handlers.
@app.errorhandler(500)
def internal_error(error):
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
