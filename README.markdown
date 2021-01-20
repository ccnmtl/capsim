[![Actions Status](https://github.com/ccnmtl/capsim/workflows/build-and-test/badge.svg)](https://github.com/ccnmtl/capsim/actions)

## Public Health Capstone Simulation (Python Version)

### requirements

* Python 3.6
* Postgres (latest)

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


