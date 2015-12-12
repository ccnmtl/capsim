APP=capsim
JS_FILES=media/js/interventions.js media/js/graph.js

all: jenkins

include *.mk

compose-migrate:
	docker-compose run web /ve/bin/python manage.py migrate --settings=capsim.settings_compose

compose-run:
	docker-compose up

notebook: ./ve/bin/python
	$(MANAGE) shell_plus --notebook
