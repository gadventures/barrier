import os

from flask import Flask, redirect, send_from_directory
from flask_oidc import OpenIDConnect
from oauth2client.client import OAuth2Credentials

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "./client-secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = os.getenv("BARRIER_SECRET_KEY")
app.config["DEFAULT_RESOURCE"] = os.getenv("BARRIER_DEFAULT_RESOURCE", "index.html")
app.config["RESOURCE_PATH"] = os.getenv("BARRIER_RESOURCE_PATH", "build/html")
oidc = OpenIDConnect(app)


@app.route("/")
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
        subject_identifier = oidc.user_getfield("sub")
        json_oidc_credentials = oidc.credentials_store[subject_identifier]
        oauth2_credentials = OAuth2Credentials.from_json(json_oidc_credentials)
        id_token_jwt = oauth2_credentials.token_response["id_token"]
        oidc_credentials_issuer_uri = oauth2_credentials.id_token["iss"]
        logout_url = f"{oidc_credentials_issuer_uri}/v1/logout?id_token_hint={id_token_jwt}"
        return redirect(logout_url)
    except KeyError:
        pass
    finally:
        oidc.logout()


@app.route("/<path:resource_path>")
@oidc.require_login
def resource_proxy(resource_path: str) -> str:
    """Safely proxy requests to files relative to the resource path."""
    return send_from_directory(app.config["RESOURCE_PATH"], resource_path.split("?")[0])


if __name__ == "__main__":
    app.run()