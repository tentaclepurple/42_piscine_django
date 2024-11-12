PROJECT_NAME=d09
APP_NAME=chat

all: env
	docker compose up -d

project:
	django-admin startproject $(PROJECT_NAME)
	@echo "Project $(PROJECT_NAME) created."


app:
	cd $(PROJECT_NAME) && python3 manage.py startapp $(APP_NAME)
	@echo "App $(APP_NAME) created inside project."

run:
	cd $(PROJECT_NAME) && python3 manage.py runserver 0.0.0.0:8000

mig:
	cd $(PROJECT_NAME) && python3 manage.py makemigrations
	cd $(PROJECT_NAME) && python3 manage.py migrate

load:
	cd $(PROJECT_NAME) && python3 manage.py loaddata $(APP_NAME)/fixtures/*.json




super:
	cd $(PROJECT_NAME) && python3 manage.py createsuperuser

#redis container
redis:
	docker run -d --name redis_server -p 6380:6379 redis

stop_redis:
	docker stop redis_server && docker rm redis_server
