from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug import abort

from tracker.db import get_db


bp = Blueprint('bugtracker', __name__)
