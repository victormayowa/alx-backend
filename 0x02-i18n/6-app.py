#!/usr/bin/env python3
"""
6-app.py
"""

from flask import Flask, render_template, g, request
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


@babel.localeselector
def get_locale():
    """Determine the user's preferred locale"""
    # Check URL parameters
    locale_from_url = request.args.get('locale')
    if locale_from_url in app.config['LANGUAGES']:
        return locale_from_url

    # Check user settings
    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    # Check request header
    locale_from_header = request.headers.get('Accept-Language')
    if locale_from_header:
        return locale_from_header.split(',')[0]

    # Default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/')
def index():
    """Render the index.html template with appropriate message status"""
    if g.user:
        welcome_message = (gettext("You are logged in as %(username)s.") %
                           {'username': g.user['name']})
    else:
        welcome_message = gettext("You are not logged in.")
    return render_template('6-index.html', welcome_message=welcome_message)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
