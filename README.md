GIFA stands for Geo Intelligence System for Flood Prone Area. An application built with Django webserver, PostgreSQL+PostGIS, and OpenDataKit (ODK) Collect to support flood prone area to prepare flood and calculate evacuation route before disaster and during disaster.

This app was built by my team (Cisitu team) during hackathon event held by https://uinspire.id/ (2019) in collaboration with West Java BPBD, BNPB, UNITAR, UNESCO. We were the 1st winner (https://uinspire.id/better_community_fix_final8-shp/) 

gifa Branch develop

All we need to get GIFA installed using this repository and running well, we need to have :
1. Linux OS
2. VirtualBox
3. Vagrant

And we also require to install :
1. Python Anaconda installed inside vagrant image
2. Apache Tomcat
3. ODK Aggregate Container

--------------------------


\# Install VirtualBox 5.x / 6.x

    https://www.virtualbox.org/wiki/Downloads

\# Install Vagrant

    https://www.vagrantup.com/downloads.html

\# Open command prompt or git bash

\# cd to source code dir and clone repo, use bionic branch for Ubuntu 18.04

    git clone https://gitlab.com/gifa.hackathon/gifa-django.git gifa
    cd gifa

\# Rename Vagrantfile.example to Vagrantfile

    cp Vagrantfile.example Vagrantfile

\# Rename db_settings.py.example to db_settings.py

    cp gifa/gifa/db_settings.py.example gifa/gifa/db_settings.py

\# Start the Vagrant VM

    vagrant up

\# Wait until first-time Vagrant provisioning completes

\# ssh to the VM and activate the gifa conda and install Django

    vagrant ssh
    curl -O https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
    sha256sum Anaconda3-2019.07-Linux-x86_64.sh
    bash Anaconda3-2019.07-Linux-x86_64.sh
    source ~/.bashrc
    conda list # Just checking
    conda update -y conda

    conda create -n gifa-django python=3.6 anaconda
    conda activate gifa-django
    cd gifa
    while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt
    nodeenv -p --prebuilt
    npm install -g bower

\# This application requires Apache Tomcat to run ODK-Aggregate Server (29 October 2019)

	for now visit https://linuxize.com/post/how-to-install-tomcat-8-5-on-ubuntu-18.04/
	we will update the steps or image on vagrantcloud

\# Create a new Django project (SKIP THIS STEP, FIRST COMMIT ONLY!!)

    django-admin startproject gifa

\# Configure Django settings file to use gifa database

    cd gifa
    nano gifa/db_settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gifa',
        'USER': 'gifa',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```
\# Run the first database migration to create Django tables

    python manage.py migrate

\# Create the superuser account (admin password123)

    python manage.py createsuperuser

\# Bower install & Collect static files

    python manage.py bower install
    python manage.py collectstatic --noinput

\# Test by running the development server

    python manage.py runserver 0.0.0.0:8000

\# On host computer browser open http://localhost:8000

\# Exit shell and shutdown VM

    exit
    vagrant halt

\# Done! To start VM again just run: vagrant up

\# To SSH to VM use the following settings

    host name: localhost
    port: 2222
    user: vagrant
    password: vagrant
