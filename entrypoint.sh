#!/bin/bash

flask db upgrade
gunicorn -w 4 -b 0.0.0.0:80 "ms:create_app()"
