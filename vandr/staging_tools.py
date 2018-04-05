import os
from functools import wraps
from flask import request, Response, flash, redirect
from vandr import app


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'admin' and password == 'noexit'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def pwd_protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if app.config['VANDR_PASSWORD_PROTECT']:
            if not auth or not check_auth(auth.username, auth.password):
                return authenticate()
        return f(*args, **kwargs)
    return decorated


# SPECIAL BACKDOOR PAGES TO SWITCH PWD_PROTECTED ON / OFF
# to circumvent the basic http authentification via pwd_protect
backdoor_secret = os.getenv('BACKDOOR_SECRET', default='')


@app.route('/pwd_unprotect__' + backdoor_secret)
def pwd_unprotect():
    # don't allow unprotection if running on production app
    if app.config['VANDR_HOME']=='https://www.vandr.at/':
        return redirect('/')

    print('\nswitching off pwd-protection!')
    app.config['VANDR_PASSWORD_PROTECT'] = False
    print(
        """app.config['VANDR_PASSWORD_PROTECT']: """,
        app.config['VANDR_PASSWORD_PROTECT'])
    flash('Password protection has been switched off',
          category='success')
    return redirect('/')


@app.route('/pwd_protect__' + backdoor_secret)
def pwd_protect():
    # don't allow to switch protection manually if running on production
    if app.config['VANDR_HOME']=='https://www.vandr.at/':
        return redirect('/')

    print('\nswitching on pwd-protection!')
    app.config['VANDR_PASSWORD_PROTECT'] = True
    print(
        """app.config['VANDR_PASSWORD_PROTECT']: """,
        app.config['VANDR_PASSWORD_PROTECT'])
    flash('Password protection has been switched on',
          category='success')
    return redirect('/')
