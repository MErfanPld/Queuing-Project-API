#!/bin/bash
pip install -r requirements.txt
python api/manage.py collectstatic --no-input --clear
