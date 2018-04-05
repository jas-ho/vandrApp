#!/bin/bash
# This file should be treated with care:
# it updates the tables of the local postgres-database
python << END
from vandr import db
from vandr.models import *
print(db)
db.create_all()
quit()
END
 
