#! /bin/bash

source venv/bin/activate
cd app/
flask run --host=0.0.0.0
#flask test
#while true; do
#    flask deploy
#    if [[ "$?" == "0" ]]; then
#        break
#    fi
#    echo Deploy command failed, retrying in 5 secs...
#    sleep 5
#done

#exec gunicorn -b :5000 --access-logfile - --error-logfile - eskimotv:frontend
