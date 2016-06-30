#!/usr/bin/python
import xmlrpclib
from flask import Flask, g, url_for, render_template, flash, session

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SPACEWALK_URL="http://mysusemanager.com/rpc/api",
    SPACEWALK_LOGIN="admin",
    SPACEWALK_PASSWORD="admin"
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def get_client():
    if not hasattr(g, 'client'):
        g.client = xmlrpclib.Server(app.config['SPACEWALK_URL'], verbose=0)
    return g.client


@app.route('/')
def hello_world():
    client = get_client()
    key = client.auth.login(app.config['SPACEWALK_LOGIN'],
                            app.config['SPACEWALK_PASSWORD'])
    entries = client.system.list_systems(key)
    client.auth.logout(key)
    return render_template('systems.html', entries=entries)


