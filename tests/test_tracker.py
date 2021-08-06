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


get_pages = [
    ('', b'There are no bugs being tracked right now.'),
    ('test', b'Hello, Dev!'),
    ('create', b'New Bug - Issue Tracker'),
    ('search', b'Search - Issue Tracker')
]


@pytest.mark.parametrize('page, text', get_pages)
def test_get_base_pages(client, page, text):
    """ Starting with a blank database """
    response = client.get(f'/{page}')
    assert text in response.data


        # project_name = request.form['project_name']     
        # bug_title = request.form['bug_title']
        # bug_description = request.form['bug_description']   
        # creator_name = request.form['creator_name']
        # assignee = request.form['assignee']
        # status = request.form['status']
        # priority = request.form['priority']

add_issues = [
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
#  (
#      {

#      }, 
#      200
#  )
]
# Test add full
@pytest.mark.parametrize('data, expected_response, expected_location', add_issues)
def test_add_message(client, data, expected_response, expected_location):
    # Response works => redirect works => 302, not 200!
    response = client.post('/create', data=data)
    assert response.status_code == expected_response
    assert response.location == expected_location


# Test add partial/required-only


# Test add bad/incomplete


# Test add wrong input names


# Test add empty


# Test read non-empty index


# Test search term


# Test update an issue; one field


# Test update multiple fields on an issue


# Test update issue without key information


# Test update issue with incorrect id


# Test update without any changes


# Test update with change field being emtpy


# Test delete an issue


# Test delete a non-existent issue


# Test deleting without an ID field



