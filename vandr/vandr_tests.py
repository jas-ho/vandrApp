from vandr import app
from flask import session
import requests, json, os, sys

import unittest
from coverage import coverage

cov = coverage(branch=True, omit=['tmp/*', 'vandr_tests.py'])
cov.start()

class VandrTestCase(unittest.TestCase):

    def setUp(self):
        vandr.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///vandr_test'
        vandr.app.config['TESTING'] = True
        vandr.app.config['SECRET_KEY'] = 'some_secret_key_'
        vandr.db.create_all()
        self.app = vandr.app.test_client()

        # active login via auth0
        json_header = {'content-type': 'application/json'}
        token_url = "https://{domain}/oauth/ro".format(domain='my_staging_account.auth0.com')
        token_payload = {
            'client_id':    'some_client_id',
            'username':     'some_username',
            'password':     'some_password',
            'id_token':     'some_id_token',
            'connection':   'Username-Password-Authentication',
            'grant_type':   'password',
            'scope':        'openid',
            'device':       'vandr_test_app'
        }
        token_info = requests.post(
            token_url,
            data=json.dumps(token_payload),
            headers = json_header).json()
        #print(token_info)

        # retrieve user info
        user_url = "https://{domain}/userinfo?access_token={access_token}" \
            .format(domain='my_staging_account.auth0.com', access_token=token_info['access_token'])
        self.user_info_dict = requests.get(user_url).json()
        print(self.user_info_dict)

        # # define session
        # print('session')
        # print(session)
        # # session['profile'] = user_info_dict
        # # session.permanent = True

    def tearDown(self):
        vandr.db.drop_all()

    def test_empty_db(self):
        print('hello test-world!')
        rv = self.app.get('/')
        #print(rv.data)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(sys.path[0], "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
