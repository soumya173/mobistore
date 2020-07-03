from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, IntegerField, FileField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Email

class AdminProfileForm(FlaskForm):
    firstname = TextField('Firstname', validators=[DataRequired(), Length(min=2, max=25)])
    lastname = TextField('Lastname', validators=[DataRequired(), Length(min=2, max=25)])
    email = TextField('Email', validators=[DataRequired(), Email()])
    mobile = TextField('Mobile', validators=[DataRequired(), Length(min=8, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class AdminUserAdd(FlaskForm):
    firstname = TextField('Firstname', validators=[DataRequired(), Length(min=2, max=25)])
    lastname = TextField('Lastname', validators=[DataRequired(), Length(min=2, max=25)])
    email = TextField('Email', validators=[DataRequired(), Email()])
    mobile = TextField('Mobile', validators=[DataRequired(), Length(min=8, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])

class AdminUserModify(FlaskForm):
    firstname = TextField('Firstname', validators=[DataRequired(), Length(min=2, max=25)])
    lastname = TextField('Lastname', validators=[DataRequired(), Length(min=2, max=25)])
    mobile = TextField('Mobile', validators=[DataRequired(), Length(min=8, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])

class AdminProductAdd(FlaskForm):
    name = TextField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    type = TextField('Type', validators=[DataRequired(), Length(min=2, max=20)])
    description = TextField('Description', validators=[DataRequired(), Length(min=2, max=40)])
    price = IntegerField('Price', validators=[DataRequired(),])
    offerid = IntegerField('Offer Id', validators=[DataRequired(),])
    file = FileField('Image File')

class AdminOfferAdd(FlaskForm):
    productid = IntegerField('productid', validators=[DataRequired(),])
    discount = IntegerField('discount', validators=[DataRequired(), NumberRange(min=0, max=100)])
    description = TextField('Description', validators=[DataRequired(), Length(min=2, max=40)])

class LoginForm(FlaskForm):
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),])