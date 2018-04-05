#!/bin/bash
# This file should be treated with care: it ereases the heroku DB and sets it up anew

heroku pg:psql --app vandr-staging << END
\d
DROP TABLE public.connexions;
DROP TABLE public.conversations;
DROP TABLE public.scores;
DROP TABLE public.invitations;
DROP TABLE public.donations;
DROP TABLE public.campaign_joins;
DROP TABLE public.users;
\q
END

heroku run python --app vandr-staging << END
from vandr import db
from vandr.models import *
from vandr.dummy_data import populate_with_dummy_data
print(db)
db.create_all()
populate_with_dummy_data(db)
quit()
END