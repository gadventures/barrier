import os
from functools import wraps
from unittest import mock

import flask_oidc
import pytest
from click.testing import CliRunner
from flask.testing import FlaskClient


@pytest.fixture
def cli_runner():
    """Generate a Click CLI Driver."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner


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
def enable_login_override():
    """Patch the OpenIDConnect client to toggle session state explicitly."""

    def mock_require_login(self, f):
        settings = {"allow_all_traffic": False}

        @wraps(f)
        def wrapped(*args, **kwargs):
            if settings["allow_all_traffic"]:
                return f(*args, **kwargs)
            else:
                return self.redirect_to_auth_server()

        wrapped.settings = settings
        return wrapped

    with mock.patch.object(flask_oidc.OpenIDConnect, "require_login", mock_require_login):
        yield


@pytest.fixture
def client(inject_secret_key, inject_client_secrets, enable_login_override) -> FlaskClient:
    """Produce a test client for barrier app."""
    from barrier.app import app

    app.config["TESTING"] = True

    with app.test_request_context():
        with app.test_client() as client:
            yield client
