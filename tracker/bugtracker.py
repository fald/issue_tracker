from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug import abort

from tracker.db import get_db


bp = Blueprint('bugtracker', __name__)


@bp.route('/')
def index():
    db = get_db()
    bugs = db.execute(
        'SELECT'
        '   i.id AS id'
        '   i.title'
        '   i.body'
        '   i.status'
        '   i.priority'
        '   i.created'
        '   i.last_modified'
        '   p.name AS project'
        '   u1.username AS creator'
        '   u2.username AS target'
        'FROM'
        '   issue i'
        '   LEFT JOIN project p ON i.project_id = p.id'
        '   LEFT JOIN user u1 ON i.creator_id = u1.id'
        '   LEFT JOIN user u2 ON i.target_id = u2.id'
        'ORDER BY'
        '   created DESC'
    ).fetchall()
    # ITS PROBABLY GREAT THAT I GO BETWEEN TRACKER, BUGS, BUGTRACKER AND ISSUES RIGHT NO PROBLEMS THERE HAHAH IM THE BEST - t. Late-night me
    return render_template('/bugs/index.html', bugs=bugs)
