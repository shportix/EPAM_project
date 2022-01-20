from flask import Blueprint
from flask_restful import Api
from api.views.main import Index

main = Blueprint('main', __name__)
api = Api(main)

api.add_resource(Index, "/")
