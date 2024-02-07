#!/usr/bin/env python3
"""
5-app.py
"""

from flask import Flask, render_template, g
from flask_babel import Babel, gettext


app = Flask(__name__)
babel = Babel(app)


# Mock user database table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Retrieve user information based on user ID"""
    return users.get(user_id)


@app.before_request
def before_request():
    """Set user information as global on flask.g.user"""
    user_id = int(request.args.get('login_as', 0))
    g.user = get_user(user_id) if user_id else None


@app.route('/')
def index():
    """Render the index.html template with appropriate messager loginstatus"""
    if g.user:
        welcome_message = (gettext("You are logged in as %(username)s.") %
                           {'username': g.user['name']})
    else:
        welcome_message = gettext("You are not logged in.")
    return render_template('5-index.html', welcome_message=welcome_message)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
