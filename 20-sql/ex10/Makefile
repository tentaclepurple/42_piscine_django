VENV_NAME=django_env
PROJECT_NAME=d06
APP_NAME=ex10

project:
	django-admin startproject $(PROJECT_NAME)
	@echo "Project $(PROJECT_NAME) created."


app:
	cd $(PROJECT_NAME) && python3 manage.py startapp $(APP_NAME)
	@echo "App $(APP_NAME) created inside project."


run:
	cd $(PROJECT_NAME) && python3 manage.py runserver


load09:
	cd $(PROJECT_NAME) && python3 manage.py loaddata $(APP_NAME)/data/ex09_initial_data.json


load10:
	cd $(PROJECT_NAME) && python3 manage.py loaddata $(APP_NAME)/data/ex10_initial_data.json


mig:
	cd $(PROJECT_NAME) && python3 manage.py makemigrations
	cd $(PROJECT_NAME) && python3 manage.py migrate


convert_json:
	cd $(PROJECT_NAME)/$(APP_NAME)/data && sed -i 's/"model": "ex09./"model": "ex09orm./g' ex09_initial_data.json


.PHONY: project app run
