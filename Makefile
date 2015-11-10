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

build:
	docker build -t ccnmtl/capsim .

compose-migrate:
	docker-compose run web python manage.py migrate --settings=capsim.settings_compose

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
