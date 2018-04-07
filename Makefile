clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

start-local-mail-server:
	python -m smtpd -n -c DebuggingServer localhost:8025
