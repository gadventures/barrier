#!/usr/bin/env python
"""Client Secrets for Barrier Service.

This script will generate ``client-secrets.json``, which will provide the credentials necessary for ``app.py` to
integrate with the OpenIDConnect service (i.e. Okta).

"""
import os
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


def convert_option_name_to_environment_variable_name(option_name: str) -> str:
    """Convert given option name to uppercase, replace hyphens with underscores, and add "BARRIER_" prefix."""
    return f"BARRIER_{option_name.upper().replace('-', '_')}"


def required_option_or_envvar(option_name: str) -> click.option:
    """Generate a required Click option with envvar support and help message."""

    def is_null(environment_variable_name):
        return environment_variable_name not in os.environ

    environment_variable_name = convert_option_name_to_environment_variable_name(option_name)
    return click.option(
        f"--{option_name}",
        envvar=environment_variable_name,
        required=is_null(environment_variable_name),
        help=f"(ENV: {environment_variable_name}) ",
    )


@required_option_or_envvar("client-id")
@required_option_or_envvar("client-secret")
@required_option_or_envvar("auth-uri")
@required_option_or_envvar("token-uri")
@required_option_or_envvar("issuer")
@required_option_or_envvar("userinfo-uri")
@required_option_or_envvar("redirect-uri")
@click.command()
def main(
    client_id: str, client_secret: str, auth_uri: str, token_uri: str, issuer: str, userinfo_uri: str, redirect_uri: str
):
    """Generate client-secrets.json in current working directory for use with Barrier service.

    You can pass the values as either CLI options and environment variables or a combination of the two. CLI options
    take precedence over environment variables when both are present.
    """
    client_secrets_json = CLIENT_SECRETS_TEMPLATE.format(**locals())
    pathlib.Path("client-secrets.json").write_text(client_secrets_json, encoding="utf-8")


if __name__ == "__main__":
    main()
