from flask import session
from vandr.forms import *
from vandr.models import *
import random, string

def create_user_record(auth0_user_id, address):
    rand_id = get_unique_rand_str()
    user_no = db.session.query(db.func.max(User.id)).scalar()
    if user_no is None:
        user_no = 0
    print('user_no')
    print(user_no)
    user = User(id=user_no+1,
                auth0_id=auth0_user_id,
                # leave nickname empty, to be chosen later
                anon_id=rand_id,
                login_count=1,
                active=True,
                email=address)
    db.session.add(user)
    db.session.commit()
    # If she was invited, save the invitation relationship in the invitation DB
    if 'invited_by_id' in session:
        inviter = User.query.filter_by(anon_id=session['invited_by_id']).one_or_none()
        invitation = Invitation(id_inviter=inviter.id, id_invitee=user.id)
        db.session.add(invitation)
        db.session.commit()
        session.pop('invited_by_id', None)
    return user

def login_update_user_record(user):
    user.login_count = user.login_count + 1
    db.session.commit()

# Update the primary points of one user
def update_primary_score(user_id):
    mys = Score.query.filter_by(id=user_id).one_or_none()
    if mys is None:
        ps = Score(id=user_id,p_total=0,p_invites=0,p_donations=0,p_campjoins=0)
        db.session.add(ps)
        db.session.commit()
        update_primary_score(user_id) # here only an entry was created, it still hast to be filled
    else:
    # Points from donation
        myd = Donation.query.filter_by(id=user_id).all()
        mys.p_donations = 0
        n_nonVal_don = 0
        for d in myd:
            if d.validated:
                mys.p_donations += d.amount
            else:
                if n_nonVal_don<3:
                    mys.p_donations += 5
                    n_nonVal_don += 1
        mys.p_donations = min(mys.p_donations,500)
    # Points from campaign join
        myj = CampaignJoin.query.filter_by(id=user_id).all()
        if len(myj)>0:
            mys.p_campjoins = 5
    # Points from conversations (convincing people)
        myc = Conversation.query.filter_by(id=user_id).all()
        mys.p_conversat = 2*len(myc)
    # Points from invites
        myi = Invitation.query.filter_by(id_inviter=user_id).all()
        mys.p_invites = 5*len(myi)
    # Update the full points
        mys.p_primary = mys.p_donations + mys.p_campjoins + mys.p_invites + mys.p_conversat
    # Commit
        db.session.commit()
    return

# Update the secondary points of one user
def update_secondary_score(user_id):
    myu = User.query.filter_by(id=user_id).first()
    mys = Score.query.filter_by(id=user_id).one_or_none()
    mys.p_secondary = 0 # start by setting the secondary points to 0

    # loop over people you invited and add 10% of their primary points
    myinv = Invitation.query.filter_by(id_inviter=user_id).all()
    for i in myinv:
        inu = Score.query.filter_by(id=i.id_invitee).one_or_none()
        mys.p_secondary += round(0.1*(inu.p_primary))

    # update the total points as well
    mys.p_total = mys.p_primary + mys.p_secondary
    myu.p_total = mys.p_total

    # commit and close
    db.session.commit()
    return

# Update the ranking of one user
def update_score_ranking(user_id):
    mys = Score.query.filter_by(id=user_id).one_or_none()
    ahead = Score.query.filter(Score.p_total > mys.p_total).all()
    mys.ranking = len(ahead) + 1
    db.session.commit()
    return

def update_all_scores():
    # Start by deleting all computed scores
    Score.query.delete()

    all_users = User.query.filter(User.active == True).all()
    # Loop through active users and compute primary score
    for u in all_users:
        update_primary_score(u.id)
    # Loop through active users and compute secondary score (and total)
    for u in all_users:
        update_secondary_score(u.id)
    # We iterate twice because the ranking has to be computed once all the users are in the table
    for u in all_users:
        update_score_ranking(u.id)
    return


def get_points_and_users(max_no=[]):
    user_points = Score.query.from_self().join(User). \
        with_entities(Score.p_total, Score.id, User.nickname,
            Score.ranking, User.active). \
        filter(User.active == True).filter(User.nickname.isnot(None)). \
        order_by(Score.p_total.desc())
    if not max_no:
        return user_points
    else:
        return user_points.limit(max_no)

def get_local_ranking(rank):

    top = 2
    bot = 2

    off = max(0,rank-top-1)
    lim = min(rank-1,top)+1+bot

    loc_rank = Score.query.from_self().join(User). \
        with_entities(Score.p_total, Score.id, User.nickname,
            Score.ranking, User.active). \
        filter(User.active == True).filter(User.nickname.isnot(None)). \
        order_by(Score.p_total.desc()).offset(off).limit(lim)
    return loc_rank

# AUX FUNCTIONS
def get_unique_rand_str():
    dup = True
    # Just to be sure that the invitation ID is unique
    while dup is not None:
        rand_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
        dup = User.query.filter_by(anon_id=rand_id).one_or_none()
    return rand_id
