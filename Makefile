postgres:
	yoyo apply -c yoyo.ini

lint:
	black .
	isort .

reapply-migrations:
	yoyo reapply -c yoyo.ini

migration:
	@read -p "Enter a migration message: " MIGRATION_MESSAGE; \
	yoyo new -c yoyo.ini --sql -m "$$MIGRATION_MESSAGE"
