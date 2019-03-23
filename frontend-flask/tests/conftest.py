import os
import tempfile

import pytest

from app import *

@pytest.fixture
def client():
    # app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    # os.unlink(app.config['DATABASE'])