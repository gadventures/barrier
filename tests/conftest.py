import os
from unittest import mock

import pytest
from flask.testing import FlaskClient


@pytest.fixture
def inject_secret_key():
    """Inject BARRIER_SECRET_KEY into environment variables."""
    os.environ["BARRIER_SECRET_KEY"] = "mock-secret-key"


@pytest.fixture
def patched_open_id_connect() -> mock.Mock:
    """Patch OpenIDConnect client."""
    with mock.patch("barrier.app.OpenIDConnect") as patched_oidc:
        yield patched_oidc


@pytest.fixture
def client() -> FlaskClient:
    """Produce a test client for barrier app."""
    from barrier.app import app

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
