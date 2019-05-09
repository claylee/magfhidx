from flask import Blueprint

fh = Blueprint("fh", __name__,template_folder='/templates')
print("fh blueprint name:",__name__)

from fh import views, errors

#from ..models import Permission
