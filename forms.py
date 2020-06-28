from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

# Set your classes here.


class AdminProfileForm(FlaskForm):
    firstname = TextField('Firstname', validators=[DataRequired(), Length(min=6, max=25)])
    lastname = TextField('Lastname', validators=[DataRequired(), Length(min=6, max=25)])
    email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])
    mobile = IntegerField('Mobile', [NumberRange(min=8, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password', message='Passwords must match')])

class AdminProductAdd(FlaskForm):
    name = TextField('Name', validators=[DataRequired(), Length(min=6, max=25)])
    type = TextField('Type', validators=[DataRequired(), Length(min=6, max=25)])
    description = TextField('Description', validators=[DataRequired(), Length(min=6, max=40)])
    price = IntegerField('Price', [NumberRange(min=8, max=10)])
    offerid = IntegerField('Offer Id', [NumberRange(min=8, max=10)])
    addedby = IntegerField('Added By', [NumberRange(min=8, max=10)])
    instock = BooleanField('In Stock?', validators=[])

class LoginForm(FlaskForm):
    email = TextField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])