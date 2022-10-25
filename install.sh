#!/bin/bash
# DEBIAN or UBUNTU like system install script

set -e

python3 -m venv venv # create virtual environment
source venv/bin/activate # activate virtual environment
pip install -r requirements.txt # install python requirements into env

# create secret keys in ENV file
cp production.env .env
echo "export SECRET_KEY=\"$(openssl rand -hex 32)\"" >> .env
echo "export CSRF_SECRET_KEY=\"$(openssl rand -hex 32)\"" >> .env

# upgrade/migrate database
flask db upgrade

# start the APP
echo "\tTo launch the virtual Environment:"
echo "source $(pwd)/venv/bin/activate"
echo "\tTo start the app after you are in the virtual Environment:"
echo "cd $(pwd)"
echo "gunicorn -w 2 \"ms:create_app()\""
