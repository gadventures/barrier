Barrier
=======

Serve static files safely behind OpenIDConnect-compatible authentication (i.e. Okta)

OpenID Connect Provider Set-up
------------------------------

Okta
~~~~

The following steps will get you the values necessary to integrate Okta with your Barrier-protected content.

#.  Go to the **Applications** section of your Okta admin app. (hint: the url of the admin app is ``https://<your organization>>-admin.okta.com/dev/console``)
#.  Click **Add Application**
#.  On the **Create New Application** page, choose **Web** and click **Next**
#.  You will need to enter some details about the application:

    *  Name: ``<your barrier-protected site name>``

    *  Base URIs: ``https://<your barrier-protected domain>/``
        *  or ``http://localhost:8000`` during development)

    *  Login redirect URIs: ``https://<your barrier-protected domain>/oidc/callback``
        *  or ``http://localhost:8000/oidc/callback``, & ``http://localhost:5000/oidc/callback`` during development

    *  Group Assigments: **Everyone** is fine, unless you have specific requirements.

    *  Grant Type Allowed:
        *  Client acting on behalf of itself
            *  ``[ ]`` Client Credentials
        *  Client acting on behalf of a user
            *  ``[x]`` Authorization Code
            *  ``[ ]`` Refresh Token
            *  ``[ ]`` Implicit (Hybrid)

#.  Click **Next** again
#.  You're now at the General Settings for your new Okta integration, scroll to the bottom and copy the **Client ID** and **Client secret** values.
#.  Visit the **Dashboard** page and copy the **Org URL**.
#.  Use the following guide to set your environment variables [1]_ :

    *  ``BARRIER_CLIENT_ID`` = **Client ID**
    *  ``BARRIER_CLIENT_SECRET`` = **Client secret**
    *  ``BARRIER_AUTH_URI`` = ``<Org URL>/oauth2/default/v1/authorize``
    *  ``BARRIER_TOKEN_URI`` = ``<Org URL>/oauth2/default/v1/token``
    *  ``BARRIER_ISSUER`` = ``<Org URL>/oauth2/default``
    *  ``BARRIER_USERINFO_URI`` = ``<Org URL>/oauth2/default/userinfo``

#. Congratulations! You're ready to install or deploy!

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


.. [1] https://developer.okta.com/blog/2018/07/12/flask-tutorial-simple-user-registration-and-login#step-1-create-an-openid-connect-config-file
