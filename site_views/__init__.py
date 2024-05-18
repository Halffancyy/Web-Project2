from flask import Blueprint

site_views = Blueprint('site_views', __name__)

from .views import *
