#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify, session, flash, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
# from flask_login import LoginManager

from utils import users
from forms import *

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'loggedin' in session and session['loggedin'] == True:
        return redirect(url_for('logout'))
    if request.method == 'GET':
        form = LoginForm(request.form)
        return render_template('forms/login.html', form=form)
    elif request.method == 'POST':
        email = request.form.get('name')
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
            return render_template('forms/login.html', form=LoginForm(request.form))

@app.route('/logout', methods=['GET'])
def logout():
    if 'loggedin' in session and session['loggedin'] == True:
        # Remove session data, this will log the user out
        session.pop('loggedin', None)
        session.pop('userid', None)
        session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' not in session or session['loggedin'] != True:
        return redirect(url_for('login'))
    userid = session['userid']
    user = users.Users()
    user_details = user.get_user_by_id(userid)
    return render_template('pages/placeholder.profile.html', user=user_details)


# @app.route('/register')
# def register():
#     form = RegisterForm(request.form)
#     return render_template('forms/register.html', form=form)


# @app.route('/forgot')
# def forgot():
#     form = ForgotForm(request.form)
#     return render_template('forms/forgot.html', form=form)

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
