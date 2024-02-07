#!/usr/bin/env python3
"""
Flask App with Internationalization, Localization, and Timezone Selection
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
import pytz


app = Flask(__name__)
babel = Babel(app)


class Config:
    """
    Configuration class for Flask app
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """
    Get user dictionary by user ID
    """
    return users.get(user_id)


def get_locale():
    """
    Get the preferred locale for the user
    """
    user_locale = request.args.get('locale')
    if user_locale and user_locale in app.config['LANGUAGES']:
        return user_locale
    if g.get('user') and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_timezone():
    """
    Get the preferred timezone for the user
    """
    user_timezone = request.args.get('timezone')
    if user_timezone:
        try:
            pytz.timezone(user_timezone)
            return user_timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.get('user') and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return 'UTC'


@app.before_request
def before_request():
    """
    Before request handler to set user in global context
    """
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.localeselector
def locale_selector():
    """
    Locale selector for Babel
    """
    return get_locale()


@babel.timezoneselector
def timezone_selector():
    """
    Timezone selector for Babel
    """
    return get_timezone()


@app.route('/')
def index():
    """
    Index route handler
    """
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
