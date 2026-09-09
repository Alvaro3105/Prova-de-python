from flask import Blueprint
from controllers.controllers import controller
from services.services import Projeto

bp = Blueprint('projetos', __name__)
