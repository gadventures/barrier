"""Barrier Application.

This script will serve serve HTTP requests and accepts any command line arguments and options that Flask applications
will accept.

"""
import os
import pathlib

from flask import Flask, redirect, send_from_directory
from flask_oidc import OpenIDConnect
from oauth2client.client import OAuth2Credentials

from .configure import RequiredEnvironmentError

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = os.getenv("BARRIER_CLIENT_SECRETS", "client-secrets.json")
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = os.getenv("BARRIER_SECRET_KEY")
app.config["DEFAULT_RESOURCE"] = os.getenv("BARRIER_DEFAULT_RESOURCE", "index.html")
app.config["RESOURCE_ROOT"] = os.getenv("BARRIER_RESOURCE_ROOT", pathlib.Path(os.getcwd()) / "build/html")


# Pre-conditions
# --------------

try:
    oidc = OpenIDConnect(app)
except FileNotFoundError:
    raise RequiredEnvironmentError("'client-secrets.json' not found. Run 'barrier-config' to create it.")
else:
    if not app.config["SECRET_KEY"]:
        raise RequiredEnvironmentError("BARRIER_SECRET_KEY not found in environment variables.")


# Routes
# ------


@app.route("/")
@oidc.require_login
def root():
    """Redirect to index.html."""
    return redirect(app.config["DEFAULT_RESOURCE"])


@app.route("/login")
@oidc.require_login
def login():
    """Redirect requests with authenticated session to default resource.

    Redirects to the OIDC login page if the request has no authentication.

    """
    return redirect(app.config["DEFAULT_RESOURCE"])


@app.route("/logout")
@oidc.require_login
def logout():
    """End the request user's OpenIDConnect-authenticated session."""
    try:
        # Get ID for request user (i.e. the 'Subject' of the credentials)
        subject_identifier = oidc.user_getfield("sub")

        # Retrieve OIDC authentication details from in-memory credentials store
        json_oidc_credentials = oidc.credentials_store[subject_identifier]
        oauth2_credentials = OAuth2Credentials.from_json(json_oidc_credentials)

        # Select the JSON Web Token (JWT) to expire with the issuer.
        id_token_jwt = oauth2_credentials.token_response["id_token"]

        # Find the base URL for the credentials issuer
        oidc_credentials_issuer_uri = oauth2_credentials.id_token["iss"]

        # Build OIDC-spec Logout URL which explicitly declares the token to expire
        logout_url = f"{oidc_credentials_issuer_uri}/v1/logout?id_token_hint={id_token_jwt}"

        # Expire local session
        oidc.logout()
        # Expire upstream session
        return redirect(logout_url)
    except KeyError:
        # Expire local session
        oidc.logout()
        # Redirect to default for login
        return redirect(app.config["DEFAULT_RESOURCE"])


@app.route("/<path:resource_path>")
@oidc.require_login
def resource_proxy(resource_path: str) -> str:
    """Safely proxy requests to files relative to the resource path."""
    return send_from_directory(app.config["RESOURCE_ROOT"], resource_path.split("?")[0])


if __name__ == "__main__":
    app.run()
