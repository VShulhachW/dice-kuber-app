# dice-kuber-app
A small app to get random dice's number in the local kubernetes.

## Prerequisites

1. Any docker engine, which could build the image (podman, docker, etc).
2. Kubernetes engine (as a part of docker, minikube, etc).
3. Installed ingress controller, for example [nginx](https://github.com/kubernetes/ingress-nginx/blob/main/docs/deploy/index.md).
4. Pyhton 3 with flask - to develop the application.

## Application

app.py:

is a Python Flask application, returns ['/health'](https://github.com/VShulhachW/dice-kuber-app/blob/main/app.py#L24) endpoint to test if the app is running. 200 - app is ready, 500 - not yet.

[/dice](https://github.com/VShulhachW/dice-kuber-app/blob/main/app.py#L18) - the main application logic, returns a number, and writes this number to log. [The example of the log's output](images/log_from_pod.png). [The application in the browser window](images/Dice_app_host.png).

## Docker image
Application could be run as a docker container. To build the app a standard docker command could be used. Flask will be installed in the process of building.
```
docker build -t diceapp:tag --file Dockerfile .
```

A built image could be pushed to any image repositiry or delivered to kubernetes by any comfortable way.

## Kubernetes deployment

Deployment.yaml file could be used to run the application as a kubernetes service.By default, application will be available on the 8000 service's port. To determine if the app is running, and if the application is healthy, the [readiness](https://github.com/VShulhachW/dice-kuber-app/blob/main/deployment.yaml#L23) and [liveness](https://github.com/VShulhachW/dice-kuber-app/blob/main/deployment.yaml#L29) probes were added.

Application logs are managed by [fluentd](https://github.com/VShulhachW/dice-kuber-app/blob/main/deployment.yaml#L34) side-car container. Logs could be checked by kubernetes command
```
kubectl logs POD_NAME -c fluentd
```

[Ingress](https://github.com/VShulhachW/dice-kuber-app/blob/main/ingress.yaml) could be configured to establish the application by the domain name, not the cluster/service address. 

The command to deploy the application:
```
kubectl apply -f deployment.yaml
kubectl apply -f ingress.yaml
```

## Monitoring as a bonus

Prometheus and Grafana could be used to monitor the application and the cluster. The steps are:

1. Deploy Grafana, using helm:
```
helm install grafana grafana/grafana -n monitoring
```

2. Install Prometheus 
```
helm install prometheus prometheus-community/prometheus --set server.persistentVolume.enabled=false -n monitoring
```

3. Add Prometheus datasource to grafana. Address should be 'http://internal-prometheus-service-address'

4. Add/build [Dashboard](images/Grafana_dashboard.png) to grafana to monitor the application.

Note: Grafana and kubernetes are set up with no mounted volumes in the local environment. That mean, that the data will be lost if the pod is deleted. For production set up it is better to keep grafana's/prometheus' data on the persistance volumes.  