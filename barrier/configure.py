#!/usr/bin/env python
"""Configure Client Secrets for Barrier Service.

This script will generate ``client-secrets.json``, which will provide the credentials necessary for ``app.py` to
integrate with the OpenIDConnect service (i.e. Okta).

"""
import pathlib

import click

CLIENT_SECRETS_TEMPLATE = """{{
  "web": {{
    "client_id": "{client_id}",
    "client_secret": "{client_secret}",
    "auth_uri": "{auth_uri}",
    "token_uri": "{token_uri}",
    "issuer": "{issuer}",
    "userinfo_uri": "{userinfo_uri}",
    "redirect_uris": [
      "{redirect_uri}"
    ]
  }}
}}
"""


class RequiredEnvironmentError(KeyError):
    """Required environment variable was not set."""


@click.option("--client-id", envvar="BARRIER_CLIENT_ID", required=True)
@click.option("--client-secret", envvar="BARRIER_CLIENT_SECRET", required=True)
@click.option("--auth-uri", envvar="BARRIER_AUTH_URI", required=True)
@click.option("--token-uri", envvar="BARRIER_TOKEN_URI", required=True)
@click.option("--issuer", envvar="BARRIER_ISSUER", required=True)
@click.option("--userinfo-uri", envvar="BARRIER_USERINFO_URI", required=True)
@click.option("--redirect-uri", envvar="BARRIER_REDIRECT_URI", required=True)
@click.command()
def main(
    client_id: str, client_secret: str, auth_uri: str, token_uri: str, issuer: str, userinfo_uri: str, redirect_uri: str
):
    """Generate client secrets file."""
    client_secrets_json = CLIENT_SECRETS_TEMPLATE.format(**locals())
    pathlib.Path("client-secrets.json").write_text(client_secrets_json, encoding="utf-8")


if __name__ == "__main__":
    main()
