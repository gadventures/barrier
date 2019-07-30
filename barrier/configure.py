#!/usr/bin/env python
"""Configure Client Secrets for Barrier Service

This script will generate ``client-secrets.json``, which will provide the credentials necessary for ``barrier.py` to
integrate with the OpenIDConnect service (i.e. Okta).

"""
import os
import pathlib

CLIENT_SECRETS_TEMPLATE = """{{
  "web": {{
    "client_id": "{BARRIER_CLIENT_ID}",
    "client_secret": "{BARRIER_CLIENT_SECRET}",
    "auth_uri": "{BARRIER_AUTH_URI}",
    "token_uri": "{BARRIER_TOKEN_URI}",
    "issuer": "{BARRIER_ISSUER}",
    "userinfo_uri": "{BARRIER_USERINFO_URI}",
    "redirect_uris": [
      "{BARRIER_REDIRECT_URI}"
    ]
  }}
}}
"""

REQUIRED_ENVIRONMENT = [
    "BARRIER_CLIENT_ID",
    "BARRIER_CLIENT_SECRET",
    "BARRIER_AUTH_URI",
    "BARRIER_TOKEN_URI",
    "BARRIER_ISSUER",
    "BARRIER_USERINFO_URI",
    "BARRIER_REDIRECT_URI",
]


def main():
    for key in REQUIRED_ENVIRONMENT:
        assert key in os.environ, f"Missing Required Environment Variable: {key}"
    client_secrets_json = CLIENT_SECRETS_TEMPLATE.format(**os.environ)
    pathlib.Path("client-secrets.json").write_text(client_secrets_json, encoding="utf-8")


if __name__ == "__main__":
    main()
