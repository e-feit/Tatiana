import os
import tempfile

import pytest

from app import *

@pytest.fixture
def client():
    # app.config['DATABASE'] = tempfile.mkstemp()
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    # os.unlink(app.config['DATABASE'])