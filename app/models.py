# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id       = db.Column(db.Integer,     primary_key=True)
    user     = db.Column(db.String(64),  unique = True)
    email    = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(500))

    def __init__(self, user, email, password):
        self.user       = user
        self.password   = password
        self.email      = email

    def __repr__(self):
        return '<User %r - %s>' % (self.id) % (self.email)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 

class Information(db.Model):
    __tablename__ = 'information'
    id       = db.Column(db.Integer,     primary_key=True)
    user_id     = db.Column(db.Integer,db.ForeignKey('user.id'))
    name    = db.Column(db.String(120), unique = True)
    gender = db.Column(db.String(5))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(5))
    message = db.Column(db.String(500))
    

    def __init__(self, user, email, password):
        self.user       = user
        self.name   = name
        self.phone      = phone

    def __repr__(self):
        return '<User %r - %s>' % (self.id) % (self.name)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 