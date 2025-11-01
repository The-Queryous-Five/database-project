from flask import Blueprint
bp = Blueprint("reviews", __name__)
from . import routes  # noqa
