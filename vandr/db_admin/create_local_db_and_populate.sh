#!/bin/bash
# This file should be treated with care:
# it updates the tables of the local postgres-database
python << END
from vandr import db
from vandr.models import *
from vandr.dummy_data import populate_with_dummy_data
print(db)
db.create_all()
populate_with_dummy_data(db)
quit()
END
 
