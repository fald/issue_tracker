import sqlite3

import pytest
from tracker.db import get_db


# Coverage isn't everything - and in fact appears to show much more
# coverage than reality.

def test_init_db(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('tracker.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])

    assert 'Initialized' in result.output
    assert Recorder.called


def test_get_close_db(app):
    with app.app_context:
        db = get_db()
        assert db is get_db()
    
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    
    assert 'closed' in str(e.value)
