import datetime
from vandr.models import *
from vandr.database import update_all_scores


def populate_with_dummy_data(db):
    # users
    user1 = User(id=1, auth0_id='auth0|random_auth_ID_34',
                 email='disintegration@brachtmema.co.uk', wants_mail=True,
                 anon_id='vztw7w73Bxuy0M', nickname='pleadableness', login_count=1)
    user2 = User(id=2, auth0_id='google-oauth2|random_auth_ID_86',
                 anon_id='C2xA6GL', nickname='missing', login_count=1,
                 email='pseudonymity@translational.co.uk', wants_mail=True)
    user3 = User(id=3, auth0_id='facebook|random_auth_ID_42',
                 anon_id='vg8hDIq3sxy', nickname='psephism',
                 login_count=1, email='interbranch@taimen.com', wants_mail=False)
    user4 = User(id=4, auth0_id='auth0|random_auth_ID_21',
                 anon_id='tarP', nickname='autoluminescence',
                 login_count=1)
    user5 = User(id=5, auth0_id='auth0|random_auth_ID_4',
                 anon_id='yRsTEAoa', nickname='snuck', login_count=2)
    user6 = User(id=6, auth0_id='google-oauth2|random_auth_ID_60',
                 anon_id='EaxlK3Hqh', nickname='hypodorian', login_count=2,
                 email='dextrad@promissory.com', wants_mail=True)
    db.session.add_all([user1, user2, user3, user4, user5, user6])
    db.session.commit()

    # invitations
    invit1 = Invitation(id_inviter=2, id_invitee=6)
    invit2 = Invitation(id_inviter=3, id_invitee=1)
    invit3 = Invitation(id_inviter=5, id_invitee=4)
    invit4 = Invitation(id_inviter=5, id_invitee=3)
    db.session.add_all([invit1, invit2, invit3, invit4])
    db.session.commit()

    # donations
    donat1 = Donation(id=3, amount=500, pay_date=datetime(2016, 8, 15),
                      timestamp=datetime(2016, 9, 10),
                      published_name='Dorcas Carrol')
    donat2 = Donation(id=5, amount=5, pay_date=datetime(2016, 8, 27),
                      timestamp=datetime(2016, 9, 14),
                      published_name='Jeneva Challenger')
    donat3 = Donation(id=4, amount=100, pay_date=datetime(2016, 8, 15),
                      timestamp=datetime(2016, 9, 28),
                      published_name='Yuette Kannel')
    donat4 = Donation(id=4, amount=20, pay_date=datetime(2016, 8, 22),
                      timestamp=datetime(2016, 9, 29),
                      published_name='Yuette Kannel')
    donat5 = Donation(id=2, amount=20, pay_date=datetime(2016, 8, 23),
                      timestamp=datetime(2016, 9, 30),
                      published_name='anonymous')
    donat6 = Donation(id=2, amount=30, pay_date=datetime(2016, 8, 23),
                      timestamp=datetime(2016, 9, 30, 12, 32),
                      published_name='anonymous')
    donat7 = Donation(id=2, amount=40, pay_date=datetime(2016, 8, 23),
                      timestamp=datetime(2016, 9, 30, 13, 54),
                      published_name='anonymous')
    db.session.add_all(
        [donat1, donat2, donat3, donat4, donat5, donat6, donat7])
    db.session.commit()

    # update the scores
    update_all_scores()
