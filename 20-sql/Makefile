EX=ex01
PROJECTNAME=d06


all: env start deploy


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
	fi


start:
	minikube start


deploy:
	kubectl apply -f postgres-deployment.yaml
	kubectl apply -f adminer-deployment.yaml


#run: forward runserver


#runserver:
#	cd $(EX)/$(PROJECTNAME) && python3 manage.py runserver &


secret:
	kubectl create secret generic postgres-secret --from-env-file=.env


get:
	kubectl get all
# 	kubectl get secret postgres-secret -o yaml
# 	kubectl get deployments
# 	kubectl get pods
# 	kubectl get services


exec_postgres:
	kubectl exec -it postgres-649d8cccd6-kndcn  -- psql -U djangouser -d djangotraining


#	create a temporal access to the adminer service
adminer:
	minikube service adminer --url

forward:
	kubectl port-forward service/adminer 30000:8080 &
	kubectl port-forward service/postgres 30432:5432 &


stop:
	kubectl scale deployment adminer --replicas=0
	kubectl scale deployment postgres --replicas=0
	minikube stop


delete:
	kubectl delete -f adminer-deployment.yaml
	kubectl delete -f postgres-deployment.yaml
	minikube delete


delete_volume:
	kubectl delete pvc postgres-pv-claim


clean:
	kubectl delete -f adminer-deployment.yaml
	kubectl delete -f postgres-deployment.yaml
	kubectl delete secret postgres-secret
	rm -f .env


.PHONY: env secret deploy get exec_postgres adminer stop delete clean