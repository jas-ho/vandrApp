import os
import psycopg2


auth0_config = {
    'domain': os.getenv('AUTH0_DOMAIN',
                        default='my_staging_account.auth0.com'),
    'client_id': os.getenv('AUTH0_CLIENT_ID',
                           default='some_id'),
    'client_secret': os.getenv('AUTH0_CLIENT_SECRET',
                               default='some_secret'),
    'deletion_token': os.getenv('AUTH0_DELETION_TOKEN',
                                default='some_token')}


def vandr_logout(VANDR_HOME):
    return ('').join(
        ['https://', auth0_config['domain'], '/v2/logout',
         '?returnTo=', VANDR_HOME, 'logout',
         '?client_id=', auth0_config['client_id']])


def vandr_redirect(VANDR_HOME):
    return ('').join(
        [VANDR_HOME, 'callback',
         '?client_id=', auth0_config['client_id']])


def database_exists(url):
    # test database connection
    try:
        psycopg2.connect(url)
        return True
    except psycopg2.OperationalError:
        print('Could not open default database at ' + url)
        return False


# DEFAULT VALUES
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'some_secret_key'
    database_url = os.getenv('DATABASE_URL', default='')
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # CUSTOM CONFIG VARIABLES (not implemented in flask)
    # prefix all custom config variables with 'VANDR_ 'for clarity
    VANDR_DEBUG_DB = False
    VANDR_PASSWORD_PROTECT = False

    VANDR_AUTH0_CLIENT_ID = auth0_config['client_id']
    VANDR_AUTH0_DOMAIN = auth0_config['domain']
    VANDR_HOME = 'https://www.vandr.at/'
    VANDR_LOGOUT = vandr_logout(VANDR_HOME)
    VANDR_REDIRECT = vandr_redirect(VANDR_HOME)


# STAGING CONFIG ON HEROKU
class StagingConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    VANDR_PASSWORD_PROTECT = True
    VANDR_HOME = 'https://vandr-staging.herokuapp.com/'
    VANDR_LOGOUT = vandr_logout(VANDR_HOME)
    VANDR_REDIRECT = vandr_redirect(VANDR_HOME)


# REVIEW CONFIG ON HEROKU
class ReviewConfig(StagingConfig):
    if 'HEROKU_APP_NAME' in os.environ:
        appname = os.environ['HEROKU_APP_NAME']
        VANDR_HOME = 'https://' + appname + '.herokuapp.com/'
        VANDR_LOGOUT = vandr_logout(VANDR_HOME)
        VANDR_REDIRECT = vandr_redirect(VANDR_HOME)


# LOCAL CONFIGS
class LocalConfig(Config):
    VANDR_HOME = 'http://127.0.0.1:5000/'
    VANDR_LOGOUT = vandr_logout(VANDR_HOME)
    VANDR_REDIRECT = vandr_redirect(VANDR_HOME)

    if 'USERNAME' in os.environ:
        user = os.environ['USERNAME']
        SQLALCHEMY_DATABASE_URI = 'postgresql:///{}'.format(user)
    elif 'USER' in os.environ:
        user = os.environ['USER']
        SQLALCHEMY_DATABASE_URI = 'postgresql:///{}'.format(user)
    else:
        SQLALCHEMY_DATABASE_URI = ''

    if not database_exists(SQLALCHEMY_DATABASE_URI):
        SQLALCHEMY_DATABASE_URI = "sqlite://"  # set up in-memory sqlite db.
        VANDR_DEBUG_DB = True


class DevelopmentConfig(LocalConfig):
    DEBUG = True
    # don't intercept redirects for the debug-toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class LocalTestingConfig(LocalConfig):
    TESTING = True

class PlotConfig(Config):
    # this is somewhat redudant as the change in the URL happens via the shell
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

