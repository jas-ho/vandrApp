import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask_sqlalchemy import SQLAlchemy
from vandr import db
from vandr.models import *
from vandr.dummy_data import populate_with_dummy_data

db.create_all() # create new tables according to spec.s in vandr.models
populate_with_dummy_data(db) # fill the temporary database with dummy data from vandr.dummy_data

quit()