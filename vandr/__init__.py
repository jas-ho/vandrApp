import os
import locale
try:
    locale.setlocale(locale.LC_ALL, 'de_at')
except:
    locale.setlocale(locale.LC_ALL, '')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_sslify import SSLify
from flask_wtf import csrf


app = Flask(__name__)
csrf.CsrfProtect(app)
sslify = SSLify(app)  # enforces SSL-encryption if app.debug==False


if os.getenv('HOSTNAME') == 'heroku-server':
    print('\nrunning on heroku-production...\n')
    app.config.from_object('vandr.config.Config')
    if os.getenv('DEBUG')=='true':
        app.debug = True
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

elif os.getenv('HOSTNAME') == 'heroku-staging':
    print('\nrunning on heroku-staging...\n')
    app.config.from_object('vandr.config.StagingConfig')

elif os.getenv('HOSTNAME') == 'heroku-review':
    print('\nrunning on heroku-review...\n')
    app.config.from_object('vandr.config.ReviewConfig')

elif os.getenv('HOSTNAME') == 'plotting':
    print ('\ngenerating plots...\n')
    app.config.from_object('vandr.config.PlotConfig')
    # change DB URI here

else:
    print('\nrunning on local host...\n')
    app.config.from_object('vandr.config.DevelopmentConfig')


if os.getenv('HOSTNAME') == 'heroku-server':
    # on production: check that we connect to the auth0-account for production-app
    assert app.config['VANDR_AUTH0_DOMAIN'] == 'my_production_account.auth0.com'

else:
    # not on production: check that we connect to the auth0-account for staging-apps
    assert app.config['VANDR_AUTH0_DOMAIN'] == 'my_staging_account.auth0.com'


print('CONFIG:\n', app.config, '\n')
print('DEBUG: ', app.debug)
print('TESTING: ', app.testing)
print('DATABASE_URL: ', app.config['SQLALCHEMY_DATABASE_URI'],'\n')


db = SQLAlchemy(app)
if app.config['VANDR_DEBUG_DB']:
    print('running in VANDR_DEBUG_DB mode...\n')
    print('Running with temporary database (sqlite in-memory)\n' +
          'CAUTION: Changes will not be persistent!')
    from vandr.models import *
    db.create_all()
    from vandr.dummy_data import populate_with_dummy_data
    # fill the temporary database with dummy values
    populate_with_dummy_data(db)

toolbar = DebugToolbarExtension(app)  # toolbar runs only if app.debug==True

import vandr.views  # this import registers all the view-functions
