from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from tracker.db import get_db, init_db, get_id_or_create


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

            # TODO: Remove once no longer necessary
            creator_name = creator_name or 'fald'
            assignee = assignee or 'fald'
            project_id = get_id_or_create('project', 'name', project_name)            
            assignee_id = get_id_or_create('user', 'username', assignee)
            creator_id = get_id_or_create('user', 'username', creator_name)

            # # TODO: Remove debug.
            # print('\n', assignee, file=sys.stderr)
            # return redirect(url_for('bugtracker.index'))

            # Insert present values into the table
            # TODO: Hmm - defaults for empty str?
            # Maybe not relevant once auth is in - creator = whoevers logged in
            # Assignee can probably be blank until its been edited in, or claimed?
            # That's probably a bad idea.
            db.execute(
                'INSERT INTO issue (project_id, title, body, creator_id, target_id, status, priority) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (project_id, bug_title, bug_description, creator_id, assignee_id, status, priority)
            )
            db.commit()

            return redirect(url_for('bugtracker.index'))

    return render_template('/bugs/create.html')


@bp.route('/search')
def search():
    return render_template('/bugs/search.html')


@bp.route('/update')
def update():
    return render_template('/bugs/update.html')
