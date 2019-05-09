from flask import Blueprint

api = Blueprint("api", __name__,template_folder='/templates')
print("api_v1 blueprint name:",__name__)

from api_v1 import view
