import os
import tempfile

import pytest

from tracker import create_app
from tracker.db import init_db, get_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode("utf8")
