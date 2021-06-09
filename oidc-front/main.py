import base64
import os
import logging
from urllib.parse import urlparse

from flask import Flask, render_template, url_for, redirect, session, json, request
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.environ.get('APP_SECRET', 'SomethingNotEntirelySecret'),
    'OIDC_CLIENT_SECRETS': './client_secrets.json',
    'OIDC_ID_COOKIE_DOMAIN': os.environ.get('COOKIE_DOMAIN', None),
    'PROXY_DOMAIN': os.environ.get('PROXY_DOMAIN', None),
    'PROXY_PORT': os.environ.get('PROXY_PORT', None),
    'OIDC_DEBUG': True,
    'OIDC_ID_TOKEN_COOKIE_SECURE': os.environ.get('COOKIE_SECURE', False),
    'OIDC_SCOPES': ["openid", "profile"],
    'OVERWRITE_REDIRECT_URI': os.environ['REDIRECT_URI'],
    'OIDC_CALLBACK_ROUTE': '/authorization-code/callback',
    'COOKIE_DOMAIN': os.environ['COOKIE_DOMAIN']
})

logger = logging.getLogger(__name__)

oidc = OpenIDConnect(app)


@app.route("/")
def home():
    return render_template("home.html", oidc=oidc)


@app.route("/login")
def login():
    bu = oidc.client_secrets['issuer'].split('/oauth2')[0]
    cid = oidc.client_secrets['client_id']
    rUri = os.environ['REDIRECT_URI']

    destination = "http://localhost:8080" if request.args.get('rd') == None else request.args.get('rd')

    state = {
        'csrf_token': session['oidc_csrf_token'],
        'destination': oidc.extra_data_serializer.dumps(destination).decode('utf-8')
    }

    return render_template("login.html", oidc=oidc, baseUri=bu, redirectUri=rUri, clientId=cid,
                           state=base64_to_str(state))


@app.route("/checkaccess")
def checkaccess():
    try:
        print(request.headers, flush=True)

        originalUrl = urlparse(request.headers.get("X-Original-Url", ""))
        splitted = originalUrl.hostname.split("-")

        # Get user infos
        info = oidc.user_getinfo(["name"])
        print("displayName ", info, " original domain", splitted[0], flush=True)

        if info["name"].lower() != splitted[0].lower():
            raise Exception('Access denied for user', info["name"])

        return "OK", 200
    except Exception as e:
        return str(e), 401


@app.route("/profile")
def profile():
    try:
        info = oidc.user_getinfo(["name"])
        return render_template("profile.html", profile=info, oidc=oidc)
    except Exception as e:
        return render_template("unauthorized.html"), 401


@app.route("/logout", methods=["POST"])
@oidc.require_login
def logout():
    oidc.logout()

    return redirect(url_for("home"))


def base64_to_str(data):
    return str(base64.b64encode(json.dumps(data).encode('utf-8')), 'utf-8')


if __name__ == '__main__':
    logger.warning(msg="Proxy config : domain {} port {}".format(app.config.get("PROXY_DOMAIN"), app.config.get("PROXY_PORT")))
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)), debug=True)
