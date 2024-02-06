# RLC_task_solution

## Description

This project is an API for managing user records. Users can register, authenticate, and create, view, update, and 
delete their records. Each record contains a title, content, tag, and information about the user who created it, 
including the date and time of creation. The project uses FastAPI to create the API, SQLAlchemy to work with the 
database, and Pydantic for data validation.


## Guide for starting

### Requirements

1. [docker](https://www.docker.com)


### Create config

```shell
cp config.yaml.template config.yaml
```


### Build image

```shell
docker compose build
```

### Up containers

```shell
docker compose up
```

### Apply migrations

```shell
docker compose exec app alembic upgrade head
```

### Run tests

```shell
docker compose exec app pytest -xvv
```
