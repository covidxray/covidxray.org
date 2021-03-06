# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, jsonify,send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User,Information
from app.forms  import LoginForm, RegisterForm,SaveForm

import os
import uuid
from .chexnet.chexnet import Xray
from .util import base64_to_pil, np_to_base64, base64_to_bytes
import numpy as np
import torch
from flask import flash
from flask_paginate import Pagination, get_page_args
x_ray = Xray()


# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/register.html', form=form, msg=msg ) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/register.html', form=form, msg=msg ) )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/login.html', form=form, msg=msg ) )

@app.route('/index.html', methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        form = SaveForm(request.form)
        msg = None
        if form.validate_on_submit():
            user_id = current_user.id
            name = request.form.get('name', '', type=str)
            gender = request.form.get('gender', '', type=str)
            age = request.form.get('age', '', type=int)
            phone = request.form.get('phone', '', type=str)
            location = request.form.get('phone', '', type=str)
            note = request.form.get('note', '', type=str)
            covid = request.form.get('covid', '', type=str)
            normal = request.form.get('normal', '', type=str)
            pneumonia = request.form.get('pneumonia', '', type=str)
            information = Information.query.filter_by(name=name).first()
            
            if information:
               msg = 'Error: User exists!' 
            else:
               if covid:
                    information =  Information(user_id,name,gender,age,phone,location,note,covid,normal,pneumonia)
                    information.save()
                    msg = "Done"     
            return render_template('layouts/default.html',
                                content=render_template( 'pages/index.html',form=form, msg=msg ,informations=information))
        return render_template('layouts/default.html',
                                content=render_template( 'pages/index.html',form=form, msg=msg ))
    else:
        return render_template('layouts/home-default.html',
                                content=render_template( 'pages/home.html') )

@app.route('/result.html', methods=['GET', 'POST'])
def results():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
       information = Information.query.filter_by(id=request.form['id_result']).first()
       db.session.delete(information)
       db.session.commit()
    
    form = SaveForm(request.form)
    information = Information.query.filter_by(user_id=current_user.id)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = information.count()
    pagination_users = get_users(offset=offset, per_page=per_page,users=information)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('layouts/default.html',content=render_template( 'pages/result.html', informations=pagination_users,page=page,per_page=per_page,pagination=pagination,form=form) )


# App main route + generic routing
@app.route('/', defaults={'path': 'home.html'})
@app.route('/<path>')
def index(path):
    if path == "home.html":
        return render_template('layouts/home-default.html',
                                content=render_template( 'pages/'+path) )
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # try to match the pages defined in -> pages/<input file>
        information = Information.query.filter_by(user_id=current_user.id).first()
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path,informations=information) )
    except:
        
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )


@app.route('/predict', methods=['POST'])
def predict():
    try:
        img = base64_to_pil(request.json)
    except Exception:
        return jsonify(error="expected string or bytes-like object"), 422

    rgb_image_np = np.array(img.convert('RGB'))
    stds = rgb_image_np.std(axis=(0, 1))
    means = rgb_image_np.mean(axis=(0, 1))
    if 35 < np.average(stds) < 95 and 60 < np.average(means) < 180:
        img_result = x_ray.predict(img)
        condition_similarity_rate = []
        if img_result['condition rate'] == []:
            return jsonify(
                result='NOT DETECTED',
                error='Invalid image'
            ), 200
        else:
            condition_similarity_rate = []
            similarity_rate = 0.0001
            types = ""
            case = "HEALTY"
            for name, prob in img_result['condition rate']:
                condition_similarity_rate.append({'y': round(float(prob), 3), 'name': name})
                if round(float(prob), 3) > similarity_rate:
                   similarity_rate = round(float(prob), 3)
                   types = name
                   if name == "COVID-19" or name == "Pneumonia":
                      case = "NOT HEALTY" 
                   else:
                      case = "HEALTY"
            return jsonify(
               prob = str(round(float(similarity_rate*100), 3))+"%",
               types = str(types),
               case = case,
               condition_similarity_rate=condition_similarity_rate
            ), 200
    else:
        file_name = "NOT_DETECTED/%s.jpg" % str(uuid.uuid4())
        return jsonify(
            result='NOT DETECTED',
            error='Invalid image'
        ), 200



# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')

def get_users(offset=0, per_page=10,users=None):
    return users[offset: offset + per_page]