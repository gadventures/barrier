import pathlib
from unittest import mock

import pytest
from barrier.configure import RequiredEnvironmentError
from flask import url_for


def test_client_secrets_json_missing():
    """Should fail to import/run service without a client-secrets.json generated by ``barrier-config``."""
    assert not pathlib.Path(
        "client-secrets.json"
    ).exists(), "Move or delete client-secrets.json before running the test suite."

    with pytest.raises(RequiredEnvironmentError, match="client-secrets.json"):
        from barrier import app  # noqa: F401


def test_secret_key_missing():
    """Should fail to import/run service without a secret key to sign/verify requests via HMAC."""
    with mock.patch("flask_oidc.OpenIDConnect"):
        with pytest.raises(RequiredEnvironmentError, match="BARRIER_SECRET_KEY"):
            from barrier import app  # noqa: F401


def test_root_route_without_session(client):
    """Should induce redirect to index.html."""
    from barrier.app import oidc

    response = client.get("/")
    assert response.status_code == 302
    assert response.location.startswith(oidc.client_secrets["auth_uri"])


def test_login_route_without_session(client):
    """Should induce redirect to login page."""
    from barrier.app import oidc

    response = client.get(url_for(".login"))
    assert response.location.startswith(oidc.client_secrets["auth_uri"])


def test_logout_route_without_session(client):
    """Should induce redirect to login page."""
    from barrier.app import oidc

    response = client.get(url_for(".logout"))
    assert response.location.startswith(oidc.client_secrets["auth_uri"])


def test_resource_proxy_route_without_session(client):
    """Should induce redirect to login page."""
    from barrier.app import oidc

    response = client.get("/test-resource.html")
    assert response.location.startswith(oidc.client_secrets["auth_uri"])


def test_root_route_with_session(client):
    """Should induce redirect to default resource."""
    from barrier.app import app, root

    root.settings["allow_all_traffic"] = True

    response = client.get(url_for(".root"))
    assert response.status_code == 302
    assert response.location.endswith(app.config["DEFAULT_RESOURCE"]), response.location


def test_login_route_with_session(client):
    """Should induce redirect to default resource."""
    from barrier.app import app, login

    login.settings["allow_all_traffic"] = True

    response = client.get(url_for(".login"))
    assert response.location.endswith(app.config["DEFAULT_RESOURCE"]), response.location


def test_logout_route_with_session(client):
    """Should allow logout."""
    from barrier.app import logout

    logout.settings["allow_all_traffic"] = True

    with pytest.raises(Exception, match="User was not authenticated"):
        client.get(url_for(".logout"))


def test_resource_proxy_route_with_session_and_no_file(client):
    """Should fail to find missing file for authenticated user."""
    from barrier.app import resource_proxy

    resource_proxy.settings["allow_all_traffic"] = True

    response = client.get("/test-resource.html")
    assert response.status_code == 404


def test_resource_proxy_route_with_session_and_existing_file(client, tmp_path):
    """Should proxy resource for authenticated user."""
    from barrier.app import app, resource_proxy

    resource_name = "test-resource.html"
    (tmp_path / resource_name).write_text("Test")
    app.config["RESOURCE_ROOT"] = str(tmp_path)
    resource_proxy.settings["allow_all_traffic"] = True

    response = client.get(f"/{resource_name}")
    assert response.status_code == 200, app.config["RESOURCE_ROOT"]
