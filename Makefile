postgres:
	yoyo apply -c yoyo.ini

lint:
	black .
	isort .

reapply-migrations:
	yoyo reapply -c yoyo.ini
