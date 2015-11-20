ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MANAGE=./manage.py
APP=capsim
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python check test flake8 jshint jscs

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: ./ve/bin/python
	$(MANAGE) jenkins --pep8-exclude=migrations

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=10

runserver: ./ve/bin/python check
	$(MANAGE) runserver

celery: ./ve/bin/python check
	$(MANAGE) celery worker

migrate: ./ve/bin/python check jenkins
	$(MANAGE) migrate

check: ./ve/bin/python
	$(MANAGE) check

shell: ./ve/bin/python
	$(MANAGE) shell_plus

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint --config=.jshintrc media/js/interventions.js media/js/graph.js

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs media/js/interventions.js media/js/graph.js

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

node_modules/jscs/bin/jscs:
	npm install jscs --prefix .

# use wheelhouse/requirements.txt as the sentinal so make
# knows whether it needs to rebuild the wheel directory or not
# has the added advantage that it can just pip install
# from that later on as well
wheelhouse/requirements.txt: requirements.txt
	mkdir -p wheelhouse
	docker run --rm \
	-v $(ROOT_DIR):/app \
	-v $(ROOT_DIR)/wheelhouse:/wheelhouse \
	ccnmtl/django.build
	cp requirements.txt wheelhouse/requirements.txt
	touch wheelhouse/requirements.txt

build: wheelhouse/requirements.txt
	docker build -t ccnmtl/capsim .

compose-migrate:
	docker-compose run web /ve/bin/python manage.py migrate --settings=capsim.settings_compose

compose-run:
	docker-compose up

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make check
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make check
	make test
	make migrate
	make flake8

notebook: ./ve/bin/python
	$(MANAGE) shell_plus --notebook

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python check jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate
