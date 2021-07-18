import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from tracker.db import get_db


bp = Blueprint('bugtracker', __name__, url_prefix='/bugs')
