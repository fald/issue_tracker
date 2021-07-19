import sqlite3

import pytest
from tracker.db import get_db


# According to coverage, almost everything was already covered
# I guess just by other tests that used the same methods? Not sure, honestly.
# Anyway, apparently the only thing in db that needs to be tested is init_db
# So database should be initialized and a message should be echo'd
def test_init_db(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('tracker.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])

    assert 'Initialized' in result.output
    assert Recorder.called
