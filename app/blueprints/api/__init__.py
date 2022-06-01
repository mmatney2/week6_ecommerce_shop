from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from .import   bs_mods_routes, routes