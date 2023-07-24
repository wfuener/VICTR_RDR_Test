### High level overview
This rest API is running Python version 3.1 with the Falcon Web Framework. It will connect with a Postgres docker container which the DDL is created via flyway.

### Running
Run `docker-compose up --build` the first time you run the code. Afterwards you can just run `docker-compose up` because the containers already have been build. Also, If you would like to run the api outside the docker container you can run `docker-compose up flyway postgres` thus specifying the database to be built only

### This solution should provide

`GET /test-data`This first endpoint only exists for demo purposes so you don't have to connect to the database to view the generated data and ids. `user_id` and `event_id` are randomly generated so you will have to run this 
to get the data the database was seeded with.

```
curl 127.0.0.1:8000/test-data 
NOTE its easier to read output if you pipe it though the jq tool e.g. curl 127.0.0.1:8000/test-data | jq

RETURNS HTTP 200
[{
    "description": "user clicked next button",
    "email": "emily@test_email.com",
    "event_id": "c800eae1-a272-4f58-be35-f24276fd18c4",
    "meta_create_ts": "2023-07-21T19:19:53.486957",
    "meta_update_ts": "2023-07-21T19:19:53.486957",
    "name": "emily",
    "title": "button click",
    "ts_description": "'button':4 'click':2 'next':3 'user':1",
    "ts_title": "'button':1 'click':2",
    "user_id": "84eedf79-1e8c-4d68-8e67-384faa67d8bb"
}]


```
<br>

`GET /event` get all the events a user has created or get a specific event 
```

curl 127.0.0.1:8000/event?event_id=ee2582fb-7686-4639-bca5-6b6ae7e86da8

RETURNS HTTP 200
 {
    "description": "test description",
    "event_id": "ee2582fb-7686-4639-bca5-6b6ae7e86da8",
    "meta_create_ts": "2023-07-21T15:47:26.252750",
    "meta_update_ts": "2023-07-21T15:47:26.252750",
    "title": "test title",
    "ts_description": "'descript':2 'test':1",
    "ts_title": "'test':1 'titl':2",
    "user_id": "93db8fcb-319d-4867-9f18-dec3ee5a2f9b"
  }
```

```
curl 127.0.0.1:8000/event?user_id=46dba1d3-4850-4dec-bb3b-d67a7daddd3c

RETURNS HTTP 200
[
  {
    "description": "keyboard added to shopping cart",
    "event_id": "a60c2575-ffdd-46f2-81f4-d5b24efc5c9c",
    "meta_create_ts": "2023-07-19T15:21:54.069200",
    "meta_update_ts": "2023-07-19T15:21:54.069200",
    "title": "added item",
    "ts_description": "'ad':2 'cart':5 'keyboard':1 'shop':4",
    "ts_title": "'ad':1 'item':2",
    "user_id": "46dba1d3-4850-4dec-bb3b-d67a7daddd3c"
  }, ...
]
```
<br>

`POST /event` create an event
```
curl -d '{"user_id": "46dba1d3-4850-4dec-bb3b-d67a7daddd3c", "title": "button click", "description": "user clicked next button"}'  -H "Content-Type: application/json" -X POST 127.0.0.1:8000/event?event_id

RETURN 201 {"event_id":"c800eae1-a272-4f58-be35-f24276fd18c4"}
```
<br>

`DELETE \event` Delete an event

```
curl -X "DELETE" 127.0.0.1:8000/event?event_id=633d5bc9-8257-4b01-8ef4-ddbf59fe7af4

RETURN HTTP 200 {"message":"deleted"}
```
<br>


`GET /search` search either title, description, or both. Do this by changing the type field to one of [title, description, or both]
```

curl -G 127.0.0.1:8000/search \
-d user_id=93db8fcb-319d-4867-9f18-dec3ee5a2f9b \
-d query=test \
-d type=both

RETURNS HTTP 200 
[
  {
    description": "test description",
    "event_id": "f1d7ce53-26eb-4cf0-bd81-c6f58a3976ae",
    "similarity": 0.21739129722118378,
    "title": "test title",
    "ts_rank": 0.0607927106320858
  }, ...
]

```


### File structure
Top level holds the docker-compose file, .env file, and postman collection. Flyway holds the DDL's. In this case it's just one sql file with two tables: user and events. events_app folder is the folder with the actual api. It is built with the falcon framework. Inside there are two folders one which holds the common code used throughout the app and the other folder holds the actual resource code running for each request.

Note: Normally I would not store .env files and passwords in github but considering this is just an exercise it doesn't matter too much. Also, if you want to connect to the database you can at 0.0.0.0:5434

Falcon framework docs: 
https://falcon.readthedocs.io/en/stable/index.html

# Why falcon framework
There are many fantastic Rest APIs in the python ecosystem each with different use cases and pro's and cons. I personally enjoy the flexibility of falcon and minimalism of falcon but that doesn't make it better or worse than other frameworks. I like being able to choose my own libraries for example to parse json with, run on PYPY instead CPython, or dip into Cython. There is much more setup required with falcon for that reason hence why if your not familiar with it might seem strange to do that extra setup work. It's obviously not necessary to for example choose your own json parser, opinionated frameworks like fastapi will choose a good one for you, but I enjoy squeezing a bit of extra speed out of all my libraries albeit is unnecessary most of the time. Falcon is also requires a bit more boilerplate code with it's object oriented design but it allows you to add more of your custom functionality to it since it doesn't abstract it away from the developer. 

