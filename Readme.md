### Running
Run `docker-compose up --build` the first time you run the code. Afterwards you can just run `docker-compose up` because the containers already have been build
### This solution should provide


### Requests
You can call the two endpoint listed below or you can import the postman collection.

### Postman 
https://learning.postman.com/docs/getting-started/importing-and-exporting-data/

### File structure
Top level holds the docker-compose file, .env file, and postman collection. Flyway holds the DDL's. In this case it's just one sql file with two tables: user and events. events_app folder is the folder with the actual api. It is built with the falcon framework. Inside there are two folders one which holds the common code used throughout the app and the other folder holds the actual resource code running for each request.

Note: Normally I would not store .env files and passwords in github but considering this is just an exercise it doesn't matter too much. Also, if you want to connect to the database you can at 0.0.0.0:5434

Falcon framework docs: 
https://falcon.readthedocs.io/en/stable/index.html

# Why falcon framework
There are many fantastic Rest APIs in the python ecosystem each with different use cases and pro's and cons. I personally enjoy the flexibility of falcon and minimalism of falcon but that doesn't make it better or worse than other frameworks. I like being able to choose my own libraries for example to parse json with, run on PYPY instead CPython, or dip into Cython. There is much more setup required with falcon for that reason hence why if your not familiar with it might seem strange to do that extra setup work. It's obviously not necessary to for example choose your own json parser, opinionated frameworks like fastapi will choose a good one for you, but I enjoy squeezing a bit of extra speed out of all my libraries albeit is unnecessary most of the time. Falcon is also requires a bit more boilerplate code with it's object oriented design but it allows you to add more of your custom functionality to it since it doesn't abstract it away from the developer. 

### api
```
GET \event?user_id
get all the events a user has created

POST \event
user_id, title, description, startime, endtime
create event

GET \event?event_id=
get event by id

DELETE \event
event_id, user_id
delete event

GET \search
```
