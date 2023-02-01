from flask import Blueprint

bp = Blueprint("main",__name__)

from app.product import routes