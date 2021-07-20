import sqlite3

import pytest
from tracker.db import get_db


def test_index(client):
    response = client.get('/')

    page_elements = [
        b'Issue Tracker',
        b'Current Issues',
        b'Create',
        b'Search',
        b'Bug List',
        b'New',
    ]

    for element in page_elements:
        assert element in response.data
