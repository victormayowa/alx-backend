#!/usr/bin/env python3
"""
3-app.py
"""

from flask import Flask, render_template, request
from flask_babel import Babel, gettext


app = Flask(__name__)
babel = Babel(app)


class Config:
    """Config class for setting up Flask app"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    Get the locale based on request's accept_languages

    Returns:
        str: The selected locale
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render the index.html template with translated strings"""
    return render_template('3-index.html',
                           title=gettext('Welcome to Holberton'),
                           header=gettext('Hello world!'))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
