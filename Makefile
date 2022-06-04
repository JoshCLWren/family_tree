postgres:
	yoyo apply -c yoyo.ini

lint:
	black .
	isort .
