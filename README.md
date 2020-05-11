# Lighthouse
![](https://github.com/RobinSiep/lighthouse/workflows/Test%20%26%20Deploy/badge.svg)

Lighthouse is a tool to manage machines over a variety of networks.

It provides hardware utilisation statistics for each client and allows the user to boot up a machine through a different machine on the same subnet. Over time Lighthouse is meant to contain various other features that will make it easier to manage your machines remotely.

## Requirements
This package requires a PostgreSQL instance with a database called `lighthouse` and a user called `lighthouse` to be setup and linked through the `local-settings.ini` file described below.

You can use [Alembic](https://alembic.sqlalchemy.org/en/latest/) to keep your database schema up-to-date.

## Installation & Usage

### Using Docker
You don't need the source code unless you want to modify the package. If you just want to run the package you can do the following:
```
docker run -t lighthouse -v .:/home/lighthouse/config mellow/lighthouse:latest
```

This expects your `local-settings.ini` to be located in your current directory.

I personally use Docker Compose to run Lighthouse. Below is an example of what your `docker-compose.yml` file could look like (with sensitive info redacted):
```
version: '3'
services:
  lighthouse:
    container_name: lighthouse
    image: mellow/lighthouse:latest
    ports:
      - "7102:7102"
    volumes:
      - .:/home/lighthouse/config
    links:
      - db
    depends_on:
      - db
  db:
    container_name: lighthouse-db
    image: postgres:11
    ports:
      - "7103:5432"
    environment:
      - POSTGRES_USER=lighthouse
      - POSTGRES_PASSWORD=<YOUR PASSWORD HERE>
      - POSTGRES_DB=lighthouse
```

### From source
```
pip install -e .
lighthouse --config <PATH TO YOUR local-settings.ini> 
```

## Configuration
Both installation methods require you to setup a `local-settings.ini` file for configuration. In this repository you can find a `local-settings.ini.dist` file. Simply rename this file to `local-settings.ini` and fill in the blanks.

## Note
This project is still very much a work in progress. Its documentation and test coverage are not up to standards.

This package is meant to be used with the packages _Lighthouse Client_ and [Lighthouse Web](https://github.com/RobinSiep/lighthouse-web). Lighthouse Client is not yet publicly available.
