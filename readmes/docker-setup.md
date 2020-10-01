## Prerequisites
The following packages are required to start developing CiviWiki:

- [Docker](https://docs.docker.com/install/)
- [Docker compose](https://docs.docker.com/compose/install/)

Below variables are also needed:

- [DJANGO SECRET KEY](https://www.miniwebtool.com/django-secret-key-generator/)
- [GOOGLE MAP KEY](https://developers.google.com/maps/documentation/javascript/get-api-key)

## Environment variables file
Execute below command:

    cp .env_sample .env
 
Then, fill `DJANGO_SECRET_KEY` and `GOOGLE_MAP_API_KEY` in `.env` file.


## Requirements
Execute docker command:

    docker-compose up


and that's it! Service should be available on address `http://0.0.0.0:8000`

## Log into docker console
Go to docker-shell to execute `./manage.py` commands by executing:

    docker exec -it civiwiki-backend /bin/bash

