import os
from unittest import mock

import pytest
from flask.testing import FlaskClient


@pytest.fixture
def inject_secret_key():
    """Inject BARRIER_SECRET_KEY into environment variables."""
    os.environ["BARRIER_SECRET_KEY"] = "mock-secret-key"


@pytest.fixture
def inject_client_secrets(tmp_path):
    """Inject BARRIER_CLIENT_SECRETS into environment variables with a temporary file path."""
    from barrier.configure import CLIENT_SECRETS_TEMPLATE

    mock_secrets = tmp_path / "client-secrets.json"
    mock_secrets.write_text(
        CLIENT_SECRETS_TEMPLATE.format(
            client_id="mock-client-id",
            client_secret="mock-client-secret",
            auth_uri="http://mock-auth-uri",
            token_uri="http://mock-token-uri",
            issuer="0123456789",
            userinfo_uri="http://mock-userinfo-uri",
            redirect_uri="http://mock-redirect-uri",
        )
    )
    os.environ["BARRIER_CLIENT_SECRETS"] = str(mock_secrets)


@pytest.fixture
def client(inject_secret_key, inject_client_secrets) -> FlaskClient:
    """Produce a test client for barrier app."""
    from barrier.app import app

    app.config["TESTING"] = True

    with app.test_request_context():
        with app.test_client() as client:
            yield client
