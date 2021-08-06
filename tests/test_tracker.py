import os
import tempfile

import pytest

from tracker import create_app
from tracker.db import init_db


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


get_pages = (
    ('', b'There are no bugs being tracked right now.'),
    ('test', b'Hello, Dev!'),
    ('create', b'New Bug - Issue Tracker'),
    ('search', b'Search - Issue Tracker')
)


@pytest.mark.parametrize('page, text', get_pages)
def test_get_base_pages(client, page, text):
    """ Starting with a blank database """
    response = client.get(f'/{page}')
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
def test_add_message(client, data, expected_response, expected_location):
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
    ('fald', b'Showing 1 result for'),
    ('Project', b'Showing 2 results for'),
    ('project', b'Showing 2 results for'),
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
    client.post('/create', data=add_issues[0][0])
    client.post('/create', data=add_issues[1][0])

    rd = client.get(f'/search?search_term={term}')
    assert expected in rd.data


# Test update an issue; one field


# Test update multiple fields on an issue


# Test update issue without key information


# Test update issue with incorrect id


# Test update without any changes


# Test update with change field being emtpy


# Test delete an issue


# Test delete a non-existent issue


# Test deleting without an ID field



