from vandr import app
from flask import request, session, redirect, render_template, flash
from flask_login import LoginManager, current_user, login_user, logout_user,\
    login_required

from vandr.auth0 import *
from vandr.database import *
from vandr.models import *
from vandr.forms import *

#---------------------------------------------------------------------
# Set up LoginManager
#---------------------------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'
login_manager.login_message = 'Bitte logge Dich ein, um auf diese Seite zu gelangen.'
login_manager.login_message_category = 'warning'
# '/' should be replaced with a site explicitly asking you to log in
# and then forwarding you to NEXT


@login_manager.user_loader
def user_loader(user_id):
    """
    user loader returns
        user (the instance of User with id==user_id) IF user_id is in users-table
        None OTHERWISE (as required by flask-login)
    """
    return User.query.get(user_id)


# AUX FUNCTIONS
# flash all error messages
def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Fehler im Feld \"%s\": %s" % (
                getattr(form, field).label.text, error), category='danger')


# add additional password protection during development
from vandr.staging_tools import pwd_protected, pwd_protect, pwd_unprotect
if app.config['VANDR_PASSWORD_PROTECT']:
    meta = pwd_protected
else:
    meta = lambda f: f


#---------------------------------------------------------------------
# The actual view-functions
#---------------------------------------------------------------------


@app.route('/callback')
@meta
def callback_handling():
    user_info_dict = auth0_query()
    session['profile'] = user_info_dict
    session.permanent = True

    # Save important information
    auth0_id = session['profile']['user_id']
    email = session['profile']['email']
    print(session['profile'])
    user = User.query.filter_by(auth0_id=auth0_id)
    user = user.filter_by(active=True)
    user = user.one_or_none()
    if user == None:
        # user not yet in DB or inactive --> create record, then log her in
        user = create_user_record(auth0_id, email)
        login_user(user)
        # first connection --> invite user to choose nickname
        flash("Willkommen bei vandr!", category='success')
        return redirect('/pickname')  # to be changed
    else:  # i.e. user already in database:
        # log her in and re-activate her account if necessary
        flash("Willkommen zurück!", category='success')
        login_update_user_record(user)
        login_user(user)
        return redirect('/dash')


# --------------------------------------------------------------------
# Call pages for which login is required
# --------------------------------------------------------------------

# When logging out, remove the profile in session
@app.route('/logout')
@meta
@login_required
def logout():
    session.pop('profile', None)
    logout_user()
    flash('Bis bald!', category='success')
    return redirect('/')


@app.route('/delete_account')
@meta
@login_required
def delete_account():
    if not current_user.anon_id == request.args.get('id'):
        flash('Ungültiger link. Dein account wurde nicht gelöscht.', category='danger')
        return redirect('/datenschutz')
    auth0_unregister(current_user)
    current_user.active = False
    current_user.email = None  # do not keep email address
    current_user.nickname = None  # delete nick s.th. other users can use it
    db.session.commit()
    session.pop('profile', None)
    logout_user()
    flash("Dein vandr-account wurde erfolgreich geschlossen und deine persönlichen Daten gelöscht. Danke für dein Engagement!",
          category='success')
    # Note: the following categories can be uesd with flash and our bootstrap.css:
    #  'success' (green), 'info' (blue), 'warning' (yellow), 'danger' (red)
    return redirect('/')


# When logging in for the first time, ask to choose nickname
@app.route('/pickname', methods=['GET', 'POST'])
@meta
@login_required
def pick_name():
    nform = NicknameForm(request.form)
    if request.method == 'POST':
        if not nform.validate_on_submit():
            flash_form_errors(nform)
            return redirect('/pickname')
        unick = User.query.filter_by(
            nickname=nform.nickname.data).one_or_none()
        if unick is None:
            current_user.nickname = nform.nickname.data
            db.session.commit()
            flash('Dein nickname wurde erfolgreich geändert.',
                  category='success')
            return redirect('/dash')
        else:
            db.session.rollback()
            return render_template('pickname.html',
                                   form=nform,
                                   kind='duplicate')
    if current_user.nickname is None:
        use_kind = 'first'
    else:
        use_kind = 'change'
    return render_template('pickname.html',
                           form=nform,
                           kind=use_kind,
                           duplicate=False)


# Generate a link to send to people for invitation
@app.route('/einladen', methods=['GET', 'POST'])
@meta
@login_required
def invite_users():
    if request.method == 'POST':
        m_bdy = ("vandr ist eine coole Webapp, mit der du dich für Van der Bellen als Bundespräsident engagieren kannst!\n\n"
                 "Um mitzumachen folge bitte diesem Link: \n {home}invited/{anon_id}".format(
                     home=app.config['VANDR_HOME'], anon_id=current_user.anon_id))
        m_sbj = "Spiel mit auf vandr"
        m_cmd = "mailto:?subject={sub}&body={body}".format(
            sub=m_sbj, body=m_bdy)
        return redirect(m_cmd)
        return render_template('dash.html')
    else:
        return render_template('dash.html')


# Register with the official campaign
@app.route('/kampagne')
@meta
@login_required
def join_campaign():
    return render_template('join_campaign.html')


@app.route('/looked_up_campaign')
@meta
@login_required
def looked_up_campaign():
    new_join = CampaignJoin(id=current_user.id)
    db.session.add(new_join)
    db.session.commit()
    return redirect('https://www.vanderbellen.at/mitmachen/')


# The user dashboard with her points, etc.
@app.route("/dash", methods=['GET', 'POST'])
@meta
@login_required
def dashboard():

    cform = ConversationForm(request.form)
    if request.method == 'POST':
        if not cform.validate_on_submit():
            flash_form_errors(cform)
            return redirect('/dash')
        new_conv = Conversation(id=current_user.id,
                                name=cform.conversation_name.data,
                                date=cform.conversation_date.data,
                                comment=cform.conversation_comment.data)


        db.session.add(new_conv)
        db.session.commit()
        flash('Vielen Dank! Hier sind 2 Punkte für Deinen Einsatz! ', category='success')
        return redirect('/dash')

    update_all_scores()
    mys = Score.query.filter_by(id=current_user.id).one_or_none()
    loc_rank = get_local_ranking(mys.ranking)
    return render_template('dash.html', mys=mys, form=cform, loc_rank=loc_rank)


# The page to donate money
@app.route('/spenden', methods=['GET', 'POST'])
@meta
@login_required
def spenden():
    dform = DonationForm(request.form)
    if request.method == 'POST':  # and form.validate():
        if not dform.validate_on_submit():
            flash_form_errors(dform)
            return redirect('/spenden')
        new_don = Donation(id=current_user.id,
                           pay_date=dform.date_donation.data,
                           amount=dform.amount_donation.data,
                           published_name=dform.published_name.data)
        db.session.add(new_don)
        db.session.commit()
        flash('Vielen Dank für Deine Spende!', category='success')
        update_primary_score(current_user.id)
        return redirect('/dash')
    return render_template('spenden.html',
                           form=dform)


# --------------------------------------------------------------------
# Call pages for which login is NOT required
# --------------------------------------------------------------------


# User was invited by someone
@app.route("/invited/<uuid>")
@meta
def invite_login(uuid):
    session['invited_by_id'] = uuid
    inviter = User.query.filter_by(anon_id=uuid).one_or_none()
    print('what we found from the inviter: ', inviter)
    # only if the inviter_id is in the DB should the procedure continue
    if inviter is not None:
        return render_template('invite.html', inviter=inviter)
    # if that's not the case, just display the homepage
    else:
        return redirect('/')


# What is vandr? What do we aim for?
@app.route('/faq')
@meta
def faq():
    return render_template('faq.html')

# How do we deal with data?
@app.route('/datenschutz')
@meta
def data_protection():
    return render_template('datenschutz.html')


# How does the game work?
@app.route('/game')
@meta
def game():
    return render_template('game.html')


# The entire hall of fame, not just the five best
@app.route('/bestenliste')
@meta
def full_list():
    user_points = get_points_and_users()
    return render_template('bestenliste.html', users=user_points)

# Contacts
@app.route('/kontakt')
@meta
def kontakt():
    return render_template('kontakt.html')

# Legal stuff
@app.route('/impressum')
@meta
def impressum():
    return render_template('impressum.html')

# feedback
@app.route('/feedback')
@meta
def feedback():
    return redirect('link_to_a_feedback_form')

# Home page
@app.route("/")
@meta
def home():
    update_all_scores()
    user_points = get_points_and_users(max_no=5)
    return render_template('home.html', users=user_points, showing_home=True)
