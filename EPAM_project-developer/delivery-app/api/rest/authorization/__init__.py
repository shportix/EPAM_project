"""
authorization blueprint
"""
from flask import Blueprint
from flask_restful import Api
from api.views.authorization import SignIn, SignOut

authorization = Blueprint('authorization', __name__)
api = Api(authorization)


api.add_resource(SignIn, '/sign_in')
api.add_resource(SignOut, '/sign_out')
