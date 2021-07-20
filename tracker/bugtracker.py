from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from tracker.db import get_db, init_db


bp = Blueprint('bugtracker', __name__)


@bp.route('/')
def index():
    db = get_db()
    bugs = db.execute(
        'SELECT '
        '   i.id AS id,'
        '   i.title,'
        '   i.body,'
        '   i.status,'
        '   i.priority,'
        '   i.created,'
        '   i.last_modified,'
        '   p.name AS project,'
        '   u1.username AS creator,'
        '   u2.username AS target '
        'FROM issue i '
        'LEFT JOIN project p ON i.project_id = p.id '
        'LEFT JOIN user u1 ON i.creator_id = u1.id '
        'LEFT JOIN user u2 ON i.target_id = u2.id '
        'ORDER BY created DESC'
    ).fetchall()

    # ITS PROBABLY GREAT THAT I GO BETWEEN TRACKER, BUGS, BUGTRACKER AND ISSUES RIGHT NO PROBLEMS THERE HAHAH IM THE BEST - t. Late-night me
    return render_template('/bugs/index.html', bugs=bugs)


@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        error = None
        project_name = request.form['project_name']     
        bug_title = request.form['bug_title']
        bug_description = request.form['bug_description']   
        creator_name = request.form['creator_name']
        assignee = request.form['assignee']
        status = request.form['status']
        priority = request.form['priority']

        if not project_name:
            error = "You need to attach this issue to a project."
        elif not bug_title:
            error = "You need a title for your bug - a brief description is enough."
        elif not bug_description:
            error = "You need to describe the bug in detail."
        
        if error is not None:
            flash(error)
        else:
            db = get_db()

            # Check if project is in DB already - if not, insert it.
            project_id = db.execute(
                # TODO: Account for capitalization differences and such.
                'SELECT id FROM project WHERE project.name = (?,)', (project_name,)
            ).fetchone()

            if project_id:
                project_id = project_id[0]
            else:
                # db = get_db() # Each cursos is only valid for one call (barring executescript)
                db.execute(
                    'INSERT INTO project (name) VALUES (?,)',
                    (project_name.lower(),)
                )
                db.commit()
                project_id = db.lastrowid

            # Check if creator (defaults to fald) + assignee (if provided) are in the DB - if not, insert.
            

            # Get the ID# from the users + project to insert into table

            # Insert present values into the tablle
        
            pass

    return render_template('/bugs/create.html')
