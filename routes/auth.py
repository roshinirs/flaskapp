from flask import Blueprint

from services.authservice import AuthService

auth = Blueprint("auth", __name__)


@auth.route('/')
def index():
    obj = AuthService()
    response = obj.index()
    print(response)
    return response


@auth.route('/login', methods=['POST', 'GET'])
def login():
    obj = AuthService()
    response = obj.login()
    return response


@auth.route('/logout')
def logout():
    obj = AuthService()
    response = obj.logout()
    return response


@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    obj = AuthService()
    response = obj.signup()
    return response
