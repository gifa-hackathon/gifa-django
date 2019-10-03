#!/usr/bin/env bash
# Root level script to set up environment for Django development on Vagrant.
# Target box: ubuntu/bionic64

echo "---------------------------------------------"
echo "Upgrading packages"
echo "---------------------------------------------"
export DEBIAN_FRONTEND=noninteractive
apt-get -y update && apt-get -y upgrade

echo "---------------------------------------------"
echo "Installing dependencies (build libs, Git, PostgreSQL, PostGIS)"
echo "---------------------------------------------"
apt-get install -y htop build-essential python-pip python-dev libpq-dev git-core libjpeg8-dev libfreetype6-dev libz-dev libjpeg-dev gettext redis-server screen

echo "---------------------------------------------"
echo "Adding PostgreSQL repo"
echo "---------------------------------------------"
if [ ! -f /etc/apt/sources.list.d/pgdg.list ]; then
    echo 'deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main' >> /etc/apt/sources.list.d/pgdg.list
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
fi
apt-get update


# Install PostgreSQL with PostGIS
apt-get install -y postgresql-11 postgresql-contrib-11 postgresql-11-postgis-2.5

# Install GeoDjango dependencies (GDAL, GEOS, PROJ.4)
apt-get install -y binutils libgeoip1 libproj-dev gdal-bin python-gdal

echo "---------------------------------------------"
echo "Configure PostgreSQL for MD5 authentication"
echo "---------------------------------------------"
if [ -f /etc/postgresql/11/main/pg_hba.conf ]; then
    cp /etc/postgresql/11/main/pg_hba.conf /etc/postgresql/11/main/pg_hba.conf.orig
    echo 'local all all md5' >> /etc/postgresql/11/main/pg_hba.conf
    echo 'host all all 0.0.0.0/0 md5' >> /etc/postgresql/11/main/pg_hba.conf
fi

if [ -f /etc/postgresql/11/main/postgresql.conf ]; then
    cp /etc/postgresql/11/main/postgresql.conf /etc/postgresql/11/main/postgresql.conf.orig
    echo "listen_addresses = '*'" >> /etc/postgresql/11/main/postgresql.conf
fi

service postgresql restart
