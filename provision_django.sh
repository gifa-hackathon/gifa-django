#!/usr/bin/env bash
# User level script to set up environment for Django development on Vagrant.
# Target box: ubuntu/bionic64

DB_NAME='gifa'
DB_USERNAME='gifa'
DB_PASSWORD='password'
POSTGRES_PASSWORD='postgres'

echo "---------------------------------------------"
echo "Creating PostGIS database"
echo "---------------------------------------------"
sudo su - postgres << START
psql -c "ALTER USER postgres WITH PASSWORD '$POSTGRES_PASSWORD';"
createdb $DB_NAME
psql -c "CREATE ROLE $DB_USERNAME WITH LOGIN ENCRYPTED PASSWORD '$DB_PASSWORD';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USERNAME;"
psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" $DB_NAME
START

echo "---------------------------------------------"
echo "Provisioning complete"
echo "---------------------------------------------"
printf "Use the following database connection settings in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '$DB_NAME',
        'USER': '$DB_USERNAME',
        'PASSWORD': '$DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '',
    }
}
"
