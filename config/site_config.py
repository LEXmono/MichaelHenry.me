import logging
from os import environ, urandom
from base64 import b64encode, b64decode

logger = logging.getLogger()


def make_secret_key():
    """Make secret key and update environment var with new key.

    Returns:
        str key
    """
    try:
        new_key = urandom(64)
        print(new_key)
        token = b64encode(new_key).decode('utf-8')
        environ['FLASK_SECRET_KEY'] = token
        if environ['FLASK_SECRET_KEY'] == b64decode(token):
            pass
    except KeyError as make_secret_e:
        logger.error("Unable to set FLASK_SECRET_KEY environment variable: "
                     "{}".format(make_secret_e))
    else:
        return new_key


def configure_app(app):

    session_secret_key = b64decode(
        environ.get(
            'FLASK_SECRET_KEY', make_secret_key()
        )
    )
    # Set default configs
    environ['APP_SETTINGS'] = app.config.root_path + \
        '/config/site_settings.cfg'
    app.config.from_envvar('APP_SETTINGS')

    # Make sure everything is set before we start
    try:
        assert isinstance(environ.get('RECAPTCHA_SECRET_KEY'), str), \
            "RECAPTCHA_SECRET_KEY not set"
        assert isinstance(environ.get('RECAPTCHA_SITE_KEY'), str), \
            "RECAPTCHA_SITE_KEY not set"
        assert isinstance(environ['GITHUB_USER'], str), \
            "GITHUB_USER not set"
        assert isinstance(environ['GITHUB_API_KEY'], str), \
            "GITHUB_API_KEY not set"
        assert isinstance(environ['RECIPIENT_EMAIL'], str), \
            "RECIPIENT_EMAIL not set"
        assert isinstance(environ['SMTP_SERVER'], str), \
            "SMTP_SERVER not set"
        assert isinstance(environ['SMTP_USER'], str), \
            "SMTP_USER not set"
        assert isinstance(environ['SMTP_PASSWORD'], str), \
            "SMTP_PASSWORD not set"
    except AssertionError as env_var_error:
        logger.error("Environment variable not set. {}".format(env_var_error))
        raise

    # Load configs from env vars.
    app.config.update(
        DEBUG=environ.get('FLASK_DEBUG_STATUS', False),
        SECRET_KEY=session_secret_key,
        RECAPTCHA_SECRET_KEY=environ.get('RECAPTCHA_SECRET_KEY'),
        RECAPTCHA_SITE_KEY=environ.get('RECAPTCHA_SITE_KEY'),
    )
