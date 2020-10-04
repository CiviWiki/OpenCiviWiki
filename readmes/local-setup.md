## Prerequisites
The following packages are required to start developing CiviWiki:

- PostgreSQL
- Redis
    - [Redis installation instructions](https://redis.io/topics/quickstart)

## Set-up
The following instructions assume you have already cloned this repository.

### Requirements
You will need a virtual environment with Python 3.7 installed.

Once your virtual environment is active, run the following command to install the requirements:

```py
pip install -r requirements.txt
```

The above command should be run in the same directory as the requirements.txt file.

### Environment variables
There are several environment variables that are needed for things to work properly:

- SUNLIGHT_API_KEY
- GOOGLE_MAP_API_KEY
- REDIS_URL (optional)
- AWS_STORAGE_BUCKET_NAME (optional)
- AWS_S3_ACCESS_KEY_ID (optional)
- AWS_S3_SECRET_ACCESS_KEY (optional)
- DATABASE_URL (optional)
- CIVIWIKI_LOCAL_NAME - database name in local PostgreSQL instance
- CIVIWIKI_LOCAL_USERNAME - username in local PostgreSQL instance with rights to database
- CIVIWIKI_LOCAL_PASSWORD - password for database user

You can save some time and declare those environmental variables all at once with a shell script. E.g.

```sh
#! /bin/bash

# CiviWiki (Django)
export DJANGO_SECRET_KEY=**********

# Third party
export SUNLIGHT_API_KEY=**********
export GOOGLE_MAP_API_KEY=**********

# PostgreSQL
export CIVIWIKI_LOCAL_NAME=civiwiki
export CIVIWIKI_LOCAL_USERNAME=civiwiki
export CIVIWIKI_LOCAL_PASSWORD=password
```

To activate all of the environment variables, e.g. on Ubuntu Linux, use the following command:

```
. setup_environment_variables.sh
```

Note the pattern is 'dot space filename.sh'

### Initial CiviWiki (Django project) set up
Once you have a working virtual environment, installed all requirements, and have set up environment variables, you are ready to populate the initial database:

```py
python manage.py migrate
```

If everything goes well, you should see a bunch of green 'OK's. Django will create the database structure for you.
