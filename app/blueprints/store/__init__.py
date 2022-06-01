from flask import Blueprint

bp = Blueprint('store', __name__, url_prefix='/store')

from . import routes, models