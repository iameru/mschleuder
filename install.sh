#!/bin/sh
# DEBIAN or UBUNTU like system install script
# Install requirements

python3 -m venv venv # create virtual environment
source venv/bin/activate # activate virtual environment

pip install -r requirements.txt # install python requirements

# create secret keys in ENV file
cp production.env .env
echo "export SECRET_KEY=\"$(openssl rand -hex 32)\"" >> .env
echo "export CSRF_SECRET_KEY=\"$(openssl rand -hex 32)\"" >> .env

# upgrade/migrate database
flask db upgrade # create and migrate the database

# start the APP
# gunicorn -w 2 "ms:create_app()" # start the app
