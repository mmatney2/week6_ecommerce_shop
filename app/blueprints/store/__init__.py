from flask import Blueprint

bp = Blueprint('store', __name__, url_prefix='')

from . import routes, models