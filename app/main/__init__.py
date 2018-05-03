__author__ = 'tonnie.lwt@gmail.com'

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

