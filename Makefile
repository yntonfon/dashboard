clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

start-local-mail-server:
	python -m smtpd -n -c DebuggingServer localhost:8025

install:
	pip install -r dev-requirements.txt
	pip install -r requirements.txt

coverage:
	coverage run --branch --source app/ -m unittest -q
	coverage html --title="Dashboard coverage report"
	coverage report -m

cloc:
	pygount --format=cloc-xml --out cloc.xml --suffix=py app/

start-dev-server:
	FLASK_APP=run.py FLASK_DEBUG=1 flask run
