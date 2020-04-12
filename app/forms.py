# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])

class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])


class SaveForm(FlaskForm):
	name    = StringField  (u'Patient name'  , validators=[DataRequired()])
	gender    = StringField  (u'Gender'  , validators=[DataRequired()])
	age       = StringField  (u'Age'  , validators=[DataRequired()])
	phone     = StringField  (u'Phone number'  , validators=[DataRequired()])
	location  = StringField  (u'Location'  , validators=[DataRequired()])
	note     = StringField  (u'Clinical notes'  , validators=[DataRequired()])
	covid     = StringField  (u'covid' )
	normal     = StringField  (u'normal')
	pneumonia     = StringField  (u'pneumonia')