#!/bin/bash
# This file should be treated with care: it ereases the local DB and sets it up anew

psql -c "DROP TABLE public.connexions"
psql -c "DROP TABLE public.conversations"
psql -c "DROP TABLE public.scores"
psql -c "DROP TABLE public.invitations"
psql -c "DROP TABLE public.donations"
psql -c "DROP TABLE public.campaign_joins"
psql -c "DROP TABLE public.users"

python populate_with_dummy_data.py