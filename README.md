# Gomden

Except where otherwise noted, everything in this repository is copyrighted by
Michael N. Gagnon, 2020, and is licensed via GPL3.

Development-environment setup instructions follow...

## Here is how I began my setup by doing some python things

    virtualenv venv
    . venv/bin/activate
    pip3.7 install flask
    pip3.7 install flask_wtf
    pip3.7 install psycopg2
    pip3.7 install itsdangerous
    pip3.7 freeze > requirements.txt

## Here is how I setup redis

https://redis.io/download

    make
    make install

## Later, when launching the app, you will need to run redis in a terminal

    redis-server

## Here is how I setup the database locally

    ssh localhost -p 2222
    sudo -u postgres psql
    postgres=# CREATE DATABASE gomdendb;
    postgres=# CREATE user gomdenuser with encrypted password 'password';
    postgres=# GRANT all privileges on database gomdendb to gomdenuser;

## Here is how I initialized the tables

    scp -P 2222 gomden.sql localhost:
    ssh localhost -p 2222
    psql gomdenuser -h 127.0.0.1 -d gomdendb -a -f gomden.sql

## If you want to log into the db as gomdenuser

    ssh localhost -p 2222
    psql gomdenuser -h 127.0.0.1 -d gomdendb -a
    gomdendb=>

And, just in case, this might come in handy:

    postgres=# \connect gomdendb


## Here is how I setup Babel

I followed some of these steps: https://ccoenraets.github.io/es6-tutorial/setup-babel/

    npm init
    npm install babel-cli babel-core --save-dev
    npm install babel-preset-es2015 --save-dev
    npm install npm-watch

### Then, I did some copy and paste on package.json

    "scripts": {
        "build": "babel --presets es2015 source/js/ -d core_gomden/static/js/my/",
        "watch": "npm-watch"
    },

and

    "watch": {
        "build": "source/js/*.js"
    }

## Every time you want to launch the system

Launch pipeline-server in Virtual Box
    
In one tab:

    . venv/bin/activate
    source export.sh
    source ~/gomden-export.sh
    python3.7 -m flask run

Another tab:

    redis-server

Another tab:

    source export.sh
    source ~/gomden-export.sh
    celery -A gomden.celery worker -l info

TODO Another tab:
    
    npm run watch

Another tab:
    
    npm run watch

Or,
    
    npm run build
