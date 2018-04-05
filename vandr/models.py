from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement

from vandr import db
from sqlalchemy import ForeignKey
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)  # a simple auto-increment-integer
    nickname    = db.Column(db.String(64), unique=True)
    auth0_id    = db.Column(db.String(64))  # used for login with auth0
    anon_id     = db.Column(db.String(64), index=True, unique=True)  # this can safely be displayed
    login_count = db.Column(db.Integer, default=1)
    created     = db.Column(db.DateTime, default=datetime.now)
    modified    = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    active      = db.Column(db.Boolean, default=True)
    email       = db.Column(db.String(64))
    wants_mail  = db.Column(db.Boolean, default=True)
    p_total     = db.Column(db.Integer)

    def get_id(self):
        """Return the id (as a string!) to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """True, as users end up in the database only after authentication."""
        return True

    def is_active(self):
        """False, if the user account has been deleted and not reopened.
        Our app should not display any information about inactive users!"""
        return self.active

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Invitation(db.Model):
    __tablename__ = 'invitations'
    id_inviter = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    id_invitee = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)

class Donation(db.Model):
    __tablename__ = 'donations'
    id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    timestamp = db.Column(db.DateTime(), primary_key=True, default=datetime.now)
    pay_date = db.Column(db.Date())
    amount = db.Column(db.Float())
    published_name = db.Column(db.String(240), default='')
    validated = db.Column(db.Boolean(), default=False)

class CampaignJoin(db.Model):
    __tablename__ = 'campaign_joins'
    id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    timestamp = db.Column(db.DateTime(), primary_key=True, default=datetime.now)

class Score(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    p_total     = db.Column(db.Integer) # primary + secondary
    p_primary   = db.Column(db.Integer) # from own actions
    p_secondary = db.Column(db.Integer) # from actions by people you invited
    p_invites   = db.Column(db.Integer)
    p_donations = db.Column(db.Integer)
    p_campjoins = db.Column(db.Integer)
    p_conversat = db.Column(db.Integer)
    ranking     = db.Column(db.Integer)

class Connexion(db.Model):
    __tablename__ = 'connexions'
    id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    timestamp = db.Column(db.DateTime(), primary_key=True, default=datetime.now)
    ip_address = db.Column(db.String(240), default='')

class Conversation(db.Model):
    __tablename__ = 'conversations' # convincing people
    timestamp = db.Column(db.DateTime(), default=datetime.now)
    id = db.Column(db.Integer, ForeignKey("users.id"), primary_key=True)
    date = db.Column(db.Date(), primary_key=True)
    name = db.Column(db.String(50), default='')
    comment = db.Column(db.String(500), default='')
