from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange

# Set your classes here.


class AdminProfileForm(FlaskForm):
    firstname = TextField('Firstname', validators=[DataRequired(), Length(min=6, max=25)])
    lastname = TextField('Lastname', validators=[DataRequired(), Length(min=6, max=25)])
    email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])
    mobile = IntegerField('Mobile', validators=[DataRequired(), NumberRange(min=8, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('Password', message='Passwords must match')])

class AdminUserAdd(FlaskForm):
    firstname = TextField('Firstname', validators=[DataRequired(), Length(min=6, max=25)])
    lastname = TextField('Lastname', validators=[DataRequired(), Length(min=6, max=25)])
    email = TextField('Email', validators=[DataRequired(), Length(min=6, max=40)])
    mobile = IntegerField('Mobile', validators=[DataRequired(), NumberRange(min=8, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])

class AdminProductAdd(FlaskForm):
    name = TextField('Name', validators=[DataRequired(), Length(min=6, max=25)])
    type = TextField('Type', validators=[DataRequired(), Length(min=6, max=25)])
    description = TextField('Description', validators=[DataRequired(), Length(min=6, max=40)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=8, max=10)])
    offerid = IntegerField('Offer Id', validators=[DataRequired(), NumberRange(min=8, max=10)])
    addedby = IntegerField('Added By', validators=[DataRequired(), NumberRange(min=8, max=10)])

class AdminOfferAdd(FlaskForm):
    productid = IntegerField('productid', validators=[DataRequired(), Length(min=1)])
    discount = IntegerField('discount', validators=[DataRequired(), Length(min=1, max=3)])
    description = TextField('Description', validators=[DataRequired(), Length(min=6, max=40)])

class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), DataRequired()])