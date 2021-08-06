import os
import tempfile

import pytest

from tracker import create_app
from tracker.db import init_db, get_db


# Pytest fixtures are to provide context for tests - a database and sample client
# So we'll make one to configure the test application and a test db ('data.sql')
@pytest.fixture
def client():
    # Temp file - keep data so we can delete it properly when done
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data = f.read().decode('utf-8')

get_pages = (
    ('', 200, b'There are no bugs being tracked right now.'),
    ('test', 200, b'Hello, Dev!'),
    ('create', 200, b'New Bug - Issue Tracker'),
    ('search', 200, b'Search - Issue Tracker'),
    ('update', 404, b'Not Found'),
    ('update/0', 404, b'Not Found'),
    ('delete', 404, b'Not Found'),
    ('delete/0', 405, b'Method Not Allowed')
)


@pytest.mark.parametrize('page, exp_status_code, text', get_pages)
def test_get_base_pages(client, exp_status_code, page, text):
    """ Starting with a blank database """
    response = client.get(f'/{page}')
    assert response.status_code == exp_status_code
    assert text in response.data


add_issues = (
    # Full
    (
        {
            'project_name': 'Project Name',
            'bug_title': 'Bug Title',
            'bug_description': 'Bug Description',
            'creator_name': 'Creator Name',
            'assignee': 'Assignee',
            'status': 'Status',
            'priority': 'Priority'
        }, 
        302,
        'http://localhost/'
    ),
    # Required-only
    (
        {
            'project_name': 'Project Name',
            'bug_title': 'Bug Title',
            'bug_description': 'Bug Description',
        }, 
        302,
        'http://localhost/'
    ),
    # Incomplete
    (
        {
            'project_name': 'Project Broken',
            'bug_title': 'Bug Title',
            'creator_id': 'Jimboni'
        },
        200,
        None
    ),
    (
        {
            'project_name': 'Project Broken',
            'bug_description': 'Bug Description',
            'creator_id': 'Jimboni'
        },
        200,
        None
    ),
    # Required...but wrong
    (
        {
            'project_nam': 'Dropped my e',
            'bug_header': 'That makes more sense',
            'bug_details': 'So does that'
        },
        200,
        None
    ),
    # Nothin'
    (
        {},
        200,
        None
    )
)

@pytest.mark.parametrize('data, expected_response, expected_location', add_issues)
def test_add_issue(client, data, expected_response, expected_location):
    # Response works => redirect works => 302, not 200!
    response = client.post('/create', data=data)
    assert response.status_code == expected_response
    # if expected_response == 302:
    assert response.location == expected_location


# Test read non-empty index
def test_read_nonempty(client):
    assert b'There are no bugs being tracked right now' in client.get('/').data
    client.post('/create', data=add_issues[0][0])
    assert b'There are no bugs being tracked right now' not in client.get('/').data


search_terms = (
    ('fald', b'Showing 2 results for'),
    ('FALd', b'Showing 2 results for'),
    ('zuse', b'Showing 1 result for'),
    ('asdadakca', b'There were 0 results for your search term.')
)

# Test search term
@pytest.mark.parametrize('term, expected', search_terms)
def test_search(client, term, expected):
    # Base search page, no messages
    rd = client.get('/search').data
    assert b'There were' not in rd
    assert b'Showing ' not in rd

    # Adding some stuff to db
    # client.post('/create', data=add_issues[0][0])
    # client.post('/create', data=add_issues[1][0])
    # Hm, way to do this without being in the inital fixture? Need it to not
    # be there so I can easily test the empty page.
    get_db().executescript(_data)

    rd = client.get(f'/search?search_term={term}')
    assert expected in rd.data


def test_update_initial(client, id=1):
    client.get('/') # dunno why I need to do this; best guess is it sets the context somehow, but.
    get_db().executescript(_data)
    response = client.get('/update/1')
    assert response.status_code == 200
    assert b'SQL Issues' in response.data


updates = (
    (1, {'bug_title': 'SQooL Ishoos'}, 302, 'http://localhost/'),
    (2, {'status': 'closed', 'assignee': 'russ'}, 302, 'http://localhost/'),
    (None, {'bug_description': 'This is going nowhere!'}, 404, None),
    ('a', {'bug_title': 'Letters as ID'}, 404, None),
    (0, {'bug_title': 'Nonexistent issue'}, 404, None),
    (1, {}, 302, 'http://localhost/'),
    (1, {'no_field': 'Hmmm'}, 302, 'http://localhost/')
)

@pytest.mark.parametrize("id, vals, expected_code, expected_redirect", updates)
def test_update(client, id, vals, expected_code, expected_redirect):
    # I apparently need to do this??
    client.get('/')
    get_db().executescript(_data)

    response = client.post(f'/update/{id}', data=vals)
    assert response.status_code == expected_code
    assert response.location == expected_redirect


deletes = (
    (1, 302, True),
    (0, 302, False),
    (5, 302, False),
    (None, 404, False)
)

@pytest.mark.parametrize('id, expected_code, expected_change', deletes)
def test_delete(client, id, expected_code, expected_change):
    client.get('/')
    db = get_db()
    db.executescript(_data)
    num_issues = db.execute(
        'SELECT COUNT(*) FROM issue'
    ).fetchone()[0]
    assert num_issues == 4

    response = client.post(f'/delete/{id}')
    assert response.status_code == expected_code

    num_issues = get_db().execute(
        'SELECT COUNT(*) FROM issue'
    ).fetchone()[0]
    
    assert num_issues == 3 if expected_change else 4
    