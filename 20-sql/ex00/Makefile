VENV_NAME=django_env
PROJECT_NAME=d06
APP_NAME=ex00 


project:
	django-admin startproject $(PROJECT_NAME)
	@echo "Project $(PROJECT_NAME) created."


app:
	cd $(PROJECT_NAME) && python3 manage.py startapp $(APP_NAME)
	@echo "App $(APP_NAME) created inside project."


run:
	cd $(PROJECT_NAME) && python3 manage.py runserver


.PHONY: project app run
