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


def test_empty_db(client):
    """ Starting with a blank database """
    response = client.get('/')
    assert b'There are no bugs being tracked right now.' in response.data
