#!/bin/bash
# This file should be treated with care: it ereases the local DB and sets it up anew
heroku run python << END
from vandr import db
from vandr.models import *
print(db)
db.create_all()
quit()
END
