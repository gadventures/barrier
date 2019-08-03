import json
import pathlib
from unittest import mock

from barrier.configure import main as configure


def validate_secrets():
    """Validate the contents of client-secrets.json."""
    client_secrets = json.loads(pathlib.Path("client-secrets.json").read_bytes())
    return all(
        (
            client_secrets["web"]["client_id"] == "test-client-id",
            client_secrets["web"]["client_secret"] == "test-client-secret",
            client_secrets["web"]["auth_uri"] == "test-auth-uri",
            client_secrets["web"]["token_uri"] == "test-token-uri",
            client_secrets["web"]["issuer"] == "test-issuer",
            client_secrets["web"]["userinfo_uri"] == "test-userinfo-uri",
            client_secrets["web"]["redirect_uris"][0] == "test-redirect-uri",
        )
    )


def test_no_environment_or_options(cli_runner):
    """Should require expected options or environment."""
    result = cli_runner.invoke(configure)
    assert result.exit_code == 2
    assert not pathlib.Path("client-secrets.json").exists()


def test_options_only(cli_runner):
    """Should produce client-secrets.json when provided all required options."""
    result = cli_runner.invoke(
        configure,
        (
            "--client-id test-client-id "
            "--client-secret test-client-secret "
            "--auth-uri test-auth-uri "
            "--token-uri test-token-uri "
            "--issuer test-issuer "
            "--userinfo-uri test-userinfo-uri "
            "--redirect-uri test-redirect-uri"
        ),
    )
    assert result.exit_code == 0
    assert pathlib.Path("client-secrets.json").exists()
    assert validate_secrets(), pathlib.Path("client-secrets.json").read_bytes()


def test_environment_only(cli_runner):
    """Should override environment variables with explicit command line options."""
    with mock.patch.dict(
        "os.environ",
        {
            "BARRIER_CLIENT_ID": "base-client-id",
            "BARRIER_CLIENT_SECRET": "base-client-secret",
            "BARRIER_AUTH_URI": "base-auth-uri",
            "BARRIER_TOKEN_URI": "base-token-uri",
            "BARRIER_ISSUER": "base-issuer",
            "BARRIER_USERINFO_URI": "base-userinfo-uri",
            "BARRIER_REDIRECT_URI": "base-redirect-uri",
        },
    ):
        result = cli_runner.invoke(
            configure,
            (
                "--client-id test-client-id "
                "--client-secret test-client-secret "
                "--auth-uri test-auth-uri "
                "--token-uri test-token-uri "
                "--issuer test-issuer "
                "--userinfo-uri test-userinfo-uri "
                "--redirect-uri test-redirect-uri"
            ),
        )

    assert result.exit_code == 0
    assert pathlib.Path("client-secrets.json").exists()
    assert validate_secrets(), pathlib.Path("client-secrets.json").read_bytes()


def test_environment_and_options(cli_runner):
    """Should override environment variables with explicit command line options."""
    with mock.patch.dict(
        "os.environ",
        {
            "BARRIER_CLIENT_ID": "base-client-id",
            "BARRIER_CLIENT_SECRET": "base-client-secret",
            "BARRIER_AUTH_URI": "base-auth-uri",
            "BARRIER_TOKEN_URI": "base-token-uri",
            "BARRIER_ISSUER": "base-issuer",
            "BARRIER_USERINFO_URI": "base-userinfo-uri",
            "BARRIER_REDIRECT_URI": "base-redirect-uri",
        },
    ):
        result = cli_runner.invoke(
            configure,
            (
                "--client-id test-client-id "
                "--client-secret test-client-secret "
                "--auth-uri test-auth-uri "
                "--token-uri test-token-uri "
                "--issuer test-issuer "
                "--userinfo-uri test-userinfo-uri "
                "--redirect-uri test-redirect-uri"
            ),
        )

    assert result.exit_code == 0
    assert pathlib.Path("client-secrets.json").exists()
    assert validate_secrets(), pathlib.Path("client-secrets.json").read_bytes()
