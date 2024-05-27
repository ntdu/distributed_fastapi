# ️⚡️ FastAPI Distributed Microserver ⚡️

## Project Description
FastAPI Distributed Microserver suggest places to travel based on country and season.

The project built on microservice architecture, compose two services: backend-api service and consumer service

Backend-api service provides endpoints to get country and season from client, and then respond travel recommendations.
Consumer service responsible for integrating with third-party to collect required informations, then send them back to the backend-api service.

We used kafka as the broker to connect two service. This architect allows us scale up horizontally by adding more consumer to broker

## Table of Content
* [Project Description](#project-description)
* [Getting Started](#getting-started)
  + [Running Locally](#running-locally)
    + [Prerequisites](#local-prerequisites) 
    + [Setup](#local-setup)
  + [Running On Docker](#running-on-docker)
    + [Prerequisites](#docker-prerequisites) 
    + [Setup](#docker-setup)
  + [Continuous Integration](#continuous-integration)
  + [Continuous Deployment](#continuous-deployment)

    

## <a id="getting-started"> Getting Started </a>


## <a id="running-locally"> Running Locally</a>

### <a id="local-prerequisites"> Prerequisites</a>
  - Python >= 3.8
  - Pip >= 18.0
  - Kafka
  - Mongo

### <a id="local-setup"> Setup</a>
tbd
### <a id="docker-setup"> Setup ENV</a>
Update configuration in:
```bash
OPENAI_API_KEY=
```

## <a id="running-on-docker"> Running On Docker</a>
### <a id="docker-prerequisites"> Prerequisites</a>
  - Docker - [Install Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)
  - Docker-compose - [Install Docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

### <a id="docker-setup"> Setup</a>
1. Build:  `docker-compose build`
2. Run: `docker-compose up`

## Usage
1. Using curl or other tools, you can send requests to the endpoints through methods defined here:
``` http://127.0.0.1:3000/```

2. Documents for testing can be found at here:
``` http://127.0.0.1:3000/docs```
![My docs](root/images/docs.png)

## <a id="continuous-integration"> Continuous Integration</a>
tbd

## <a id="continuous-deployment"> Continuous Deployment</a>
tbd