#!/usr/bin/env bash
mkdir -p /var/lock/provision
export DEBIAN_FRONTEND=noninteractive

echo Bla for the Win

# Instaling the Ubuntu needed packages
apt-get update

if [ ! -f /var/lock/provision/python_pip ]; then
    apt-get install -y -q python-pip python-dev
    if [ $? == 0 ]; then
        touch /var/lock/provision/python_pip
    fi
fi

if [ ! -f /var/lock/provision/mongodb ]; then
    apt-get install -y -q mongodb
    if [ $? == 0 ]; then
        touch /var/lock/provision/mongodb
    fi
fi

# Instaling the nessery python packages (via pip)

if [ ! -f /var/lock/provision/python_env ]; then
    pip install -r /localbudgets/requirements.txt
    if [ $? == 0 ]; then
        touch /var/lock/provision/python_env
    fi
fi


# starting the mongodb service
service mongodb start

# Updating the DB 
cd /localbudgets
python manage.py upload_budget

# Runing the django server
echo Running django server at 127.0.0.1:8000
python manage.py runserver 0.0.0.0:8000 2>&1
