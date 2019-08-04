Barrier
=======

Serve static files safely behind OpenIDConnect-compatible authentication (i.e. Okta)

Installation
------------

.. code::

    $ pip install (--user) https://github.com/gadventures/barrier

Commands
--------

The following is a brief overview, but you can call any of these commands with ``--help`` for more information.

``barrier-config``
    Generate "client-secrets.json", required for running the other commands. See the help text for required options. Options passed on the command line will override any values set in the environment.
``barrier-dev``
    Flask development server. Useful if extending this project to add more features.
``barrier-wsgi``
    Gunicorn WSGI wrapper. Can be placed behind nginx, Apache, or whatever you like.

Environment
-----------

Required
~~~~~~~~

+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| Name                        | Description                                                     | Where to get it                                                                           |
+=============================+=================================================================+===========================================================================================+
| ``BARRIER_USERINFO_URI``    | UserInfo URI. Part of OpenIDConnect secrets configuration.      | OpenID Connect Provider                                                                   |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| ``BARRIER_ISSUER``          | Issuer ID. Part of OpenIDConnect secrets configuration.         | OpenID Connect Provider                                                                   |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| ``BARRIER_TOKEN_URI``       | Token URI. Part of OpenIDConnect secrets configuration.         | OpenID Connect Provider                                                                   |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| ``BARRIER_AUTH_URI``        | Auth URI. Part of OpenIDConnect secrets configuration.          | OpenID Connect Provider                                                                   |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| ``BARRIER_CLIENT_SECRET``   | Client Secret Key. Part of OpenIDConnect secrets configuration. | OpenID Connect Provider                                                                   |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| ``BARRIER_CLIENT_ID``       | Client ID. Part of OpenIDConnect secrets configuration.         | OpenID Connect Provider                                                                   |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| ``BARRIER_REDIRECT_URI``    | Redirect URI. Part of OpenIDConnect secrets configuration.      | OpenID Connect Provider, The value to set is: ``https://{your-hostname}/oidc/callback``   |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+
| ``BARRIER_SECRET_KEY``      | Used for HMAC Authentication. Generate a long random string.    | Any source of random information                                                          |
+-----------------------------+-----------------------------------------------------------------+-------------------------------------------------------------------------------------------+

Optional
~~~~~~~~

+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| Name                           | Description                                                                                                                                                                                                    | Where to get it                                                                                              |
+================================+================================================================================================================================================================================================================+==============================================================================================================+
| ``BARRIER_RESOURCE_ROOT``      | Root path of static files to serve. (Default: ``build/html``)                                                                                                                                                  | Wherever you choose to add the static files in your custom layer, or add your files to the default location. |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| ``BARRIER_DEFAULT_RESOURCE``   | The file/path that users will be redirected to after login. (Default: ``index.html``)                                                                                                                          | Probably not necessary to change this.                                                                       |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
| ``BARRIER_CLIENT_SECRETS``     | OpenIDConnect secrets configuration file location. If your provider allows automatic configuration download and has a different filename, override with that filename here. (Default: ``client-secrets.json``) | OpenID Connect Provider                                                                                      |
+--------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------+
