PROJECT_NAME=ReadersCorner
APP_NAME=articles

all: env
	docker compose up -d

project:
	django-admin startproject $(PROJECT_NAME)
	@echo "Project $(PROJECT_NAME) created."


app:
	cd $(PROJECT_NAME) && python3 manage.py startapp $(APP_NAME)
	@echo "App $(APP_NAME) created inside project."

run:
	cd $(PROJECT_NAME) && python3 manage.py runserver

mig:
	cd $(PROJECT_NAME) && python3 manage.py makemigrations
	cd $(PROJECT_NAME) && python3 manage.py migrate

load:
	cd $(PROJECT_NAME) && python3 manage.py loaddata $(APP_NAME)/fixtures/*.json


super:
	cd $(PROJECT_NAME) && python3 manage.py createsuperuser

test:
	cd $(PROJECT_NAME) && python3 manage.py test $(APP_NAME)

env:
	@if [ -f .env ]; then \
		echo ".env file already exists. Skipping .env creation."; \
	else \
		echo "Enter your Postgres DB name for Django training:"; \
		read db; \
		echo "POSTGRES_DB=$$db" > .env; \
		echo "Enter your Postgres username for Django user:"; \
		read user; \
		echo "POSTGRES_USER=$$user" >> .env; \
		echo "Enter your Postgres password. Keep it secret:"; \
		read pass; \
		echo "POSTGRES_PASSWORD=$$pass" >> .env; \
		echo "Enter Postgres host:"; \
		read host; \
		echo "POSTGRES_HOST=$$host" >> .env; \
		echo "Enter Postgres port:"; \
		read port; \
		echo "POSTGRES_PORT=$$port" >> .env; \
	fi

down:
	docker compose down

exec:
	docker exec -it python bash

postgres:
	docker exec -it postgres psql -U imontero -d piscineds -h localhost -W

clean: down
	yes | docker system prune -a


#py manage.py makemessages -l es
#py manage.py compilemessages
