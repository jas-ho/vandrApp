#!/bin/bash
# This file should be treated with care: it ereases the local DB and sets it up anew

sudo -u $USER psql -c "DROP TABLE public.connexions"
sudo -u $USER psql -c "DROP TABLE public.conversations"
sudo -u $USER psql -c "DROP TABLE public.scores"
sudo -u $USER psql -c "DROP TABLE public.invitations"
sudo -u $USER psql -c "DROP TABLE public.donations"
sudo -u $USER psql -c "DROP TABLE public.campaign_joins"
sudo -u $USER psql -c "DROP TABLE public.users"

sudo -u $USER python populate_with_dummy_data.py
