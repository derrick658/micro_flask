#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user

from application.controllers import auth, user, todo
from application.models.user import User

all_bp = [
    auth.auth_bp,
    user.user_bp,
    todo.todo_bp
]

user_bp = Blueprint('user', __name__, url_prefix='')


@user_bp.route('/login', methods=['POST'])
def login():
    info = json.loads(request.data)
    username = info.get('username', 'guest')
    password = info.get('password', '')

    user = User.objects(name=username, password=password).first()
    if user:
        login_user(user)
        return jsonify(user.to_json())
    else:
        return jsonify({"status": 401, "reason": "Username or Password Error"})


@user_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(**{'result': 200, 'data': {'message': 'logout success'}})


@user_bp.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"result": 200, "data": current_user.to_json()}
    else:
        resp = {"result": 401, "data": {"message": "user no login"}}
    return jsonify(**resp)
