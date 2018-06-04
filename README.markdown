[![Build Status](https://travis-ci.org/ccnmtl/capsim.svg?branch=master)](https://travis-ci.org/ccnmtl/capsim) [![Greenkeeper badge](https://badges.greenkeeper.io/ccnmtl/capsim.svg)](https://greenkeeper.io/)

## Public Health Capstone Simulation (Python Version)

### requirements

* Python 2.7
* PostgreSQL 9.1+
* developed on Ubuntu 12.04. may run on other platforms.

### install

install dependencies:

    $ ./bootstrap.py

run the unit tests:

    $ ./manage.py jenkins

set up the database:

    $ createdb capsim
    $ ./manage.py syncdb --migrate

run web app:

    $ ./manage.py runserver

Then point your browser at http://localhost:8000/


