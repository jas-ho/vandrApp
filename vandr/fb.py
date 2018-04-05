from flask import *
import json


from flask import Flask, request, jsonify, session, redirect, render_template,\
    send_from_directory, copy_current_request_context, flash, url_for
#from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager, current_user, login_user, logout_user,\
#    login_required
#from flask_debugtoolbar import DebugToolbarExtension
import requests, json, datetime



TOKEN='some_token'

def user_likes_page(user_id, page_id):
    """
        Returns whether a user likes a page
    """
    url = 'https://graph.facebook.com/%d/likes/%d/' % (user_id, page_id)
    parameters = {'access_token': TOKEN}
    r = requests.get(url, params = parameters)
    result = json.loads(r.text)
    if result:
       data = result['data']

    if data:  #  and data[0]['created_time']
        print data
        return True
    else:
        return False


if __name__ == '__main__':
    user=insert_some_user_id_here
    uhbp=138508202860897
    _test = user_likes_page(user, uhbp)
    if _test:
        print ("user likes UNSEREN HERRN BUNDESPRAESIDENTEN")
    aldi=301598246599356
    _aldi = user_likes_page(user, aldi)
    if _aldi:
        print ("shops at ALDI")
    else:
        print ("not particularly fond of ALDI")
