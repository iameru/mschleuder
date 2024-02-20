#!/bin/bash
# DEBIAN or UBUNTU like system install script

set -e


echo "----------- :)  :) -----------"
echo "  Installing Möhrenschleuder"
echo "    --- --- ==  == --- ---    "
echo
echo "installing virtual environment"
echo "------------------------------"

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo
echo "creating environment file"
echo "------------------------------"
cp production.env .env
echo "export SECRET_KEY=\"$(openssl rand -hex 32)\"" >> .env
echo "export CSRF_SECRET_KEY=\"$(openssl rand -hex 32)\"" >> .env
echo "generated and added secretkeys to .env file"

echo
echo "upgrade or migrate database"
echo "------------------------------"
flask db upgrade

echo
echo "hints on what to do next"
echo "------------------------------"
echo "To launch the virtual Environment:"
echo "  - source $(pwd)/venv/bin/activate"
echo
echo "It is recommended to use the systemd service file."
echo "To start the app manually after you are in the virtual Environment"
echo "  - cd $(pwd)"
echo "  - gunicorn -w 2 \"ms:create_app()\""

echo
echo "finished successully"
echo "------------------------------"
