# CourseEvaluation
We would like to design a website where students can post their opinion about a teacher. This website should have following functions: 1.     Clients can sign up a new account 2.     Clients can post evaluation under courses they attended 3.     Clients can view other students’ evaluation



## Setup and run the application

### Setup and run the backend
The backend application is created based on Flask - a web service framework from Python ecosystem, so, a python environment need to be installed before run the application.
#### Setup Python and PIP
Just download Python from its official site and install it.
Also pip has already been packaged inside Python since latest version, it is better to install one from pip's official site if the OS is Mac OSX.

#### Setup dependencies
Run the following command to install all dependencies:
```
pip install -r requirements.txt
```

> IMPORTANT: Don't forget update requirements.txt once we add/remove python dependencies such as Flask, SQLAlchemy, etc.


#### Start the backend
Run the following command to start the backend server:
```
python backup.py
```


### Setup and run the frontend

Just open the index.html from a browser.

In case of changing something in the source codes, you can rebuild the html files with necessary JS files by the following steps:
1. Install NodeJS and Yarn
2. From the project folder run the following commands.
    ```
    yarn install
    grunt build
    ```



### Demo multiple services through Docker

#### Install Docker
Reference to [official site](https://www.docker.com/community-edition).

#### Start/stop all containers to demo
```
# start
docker-compose -p ce up -d --scale consul=3

# stop
docker-compose -p ce down

# List
docker-compose -p ce ps
```

#### Do not start Backend until Consul server is ready
Refer to [Control startup order in Compose](https://docs.docker.com/compose/startup-order/), 
choose the [wait-for](https://github.com/Eficode/wait-for) as the solution.


#### Use Message Queue to simulat CQRS - Command Query Responsibility Segeration
Instead of recording API visits into Redis directly from the Backend server, send a visiting event to Kafka.
A new microservice - consumer.py - will be listening to those events and incr API usages in Redis.

someone provides a python lib for access kafka https://github.com/dpkp/kafka-python

#### Start a simplest web server from a official python container
```
# 在当前目录内创建一个简单的网页 - index.html
docker run -d --name web -p 8000:8000 -v "$PWD":/app -w /app python:alpine python -m http.server 8000
# 在浏览器中访问 http://localhost:8000 应该出现刚刚创建的网页内容
```
Similar to this, we can split backend.py into multiple python programs. then start them in their own docker containers respectively.

#### Build a Custom Python Docker Image
We need a custom docker image to run our own python app since they require flask and many other python libraries.
Assume we want the name of the image to be "ce-server", then from our project root directory run the following docker command to build our image.
```
docker build -t consul-python .
```

#### Service Registry Service
Choose Consul for simplicity by leverage Docker official Consul image.

```
docker run --rm --name consul -p 8500:8500 -p 8400:8400 consul agent -server -bootstrap -client 0.0.0.0 -ui
```

# run as a client
docker run --rm --name consul1 --link consul consul agent -bind=0.0.0.0 -retry-join=consul
```
Then consul will provide a simple UI at http://localhost:8500, access it to make sure the installation is successful.

#### Start backend services
```
docker run -it --rm --name backend -p 5000:5000 -v "$PWD":/app -w /app ce-server python backend.py
```


#### Query service address

##### From DNS
1. Query IP from A record
```
docker exec ce_consului_1 dig @172.20.0.2 -p 8600 redis.service.consul

# See only answer part:
docker exec ce_consului_1 dig +noall +answer @172.20.0.2 -p 8600 redis.service.consul
```
2. Query port from SRV record
```
docker exec ce_consului_1 dig srv +noall +answer @172.20.0.2 -p 8600 redis.service.consul
```

