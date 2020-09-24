import os
import time
import requests
from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth
from requests.auth import HTTPDigestAuth as new_auth

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET KEY'] = 'secret key here'
app.secret_key = b'aller#11'

auth = HTTPDigestAuth()


users = { 'vcu': 'rams' }

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

db = SQLAlchemy(app)

class ValidationError(ValueError):
    pass

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message':'Page Not Here'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message': 'Something is Broken'}), 500

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.route('/ping', methods=['GET'])
@auth.login_required
def ping_service():
    url = 'https://authorization-testing.herokuapp.com/pong'
    r = requests.get(url, auth=new_auth('vcu', 'rams'))
    pingpong_t = g.request_time()
    return jsonify({'request time elapsed': pingpong_t}), 201

@app.errorhandler(401)
def authorization_error(e):
    return jsonify({'request time elapsed': pingpong_t}), 201

@app.route('/pong', methods=['GET'])
@auth.login_required
def pong_service():
    return jsonify({'message': 'Hello, user!'}), 201
