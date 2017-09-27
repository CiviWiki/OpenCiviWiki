# Set-up instructions
Use these instructions to set up a local development environment.

## Prerequisites
The following packages are required to start developing CiviWiki:

- PostgreSQL
- Redis
    - [Redis installation instructions](https://redis.io/topics/quickstart)

## Set-up
The following instructions assume you have already cloned this repository.

### Requirements
You will need a virtual environment with Python 2.7 installed.

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

### Populate initial data
There are two files, located in the `/data` directory, that contain initial categories and congressional data. Run the following commands to initialize the congressional and categories data:

```py
python manage.py loaddata data/congress.json
```

```py
python manage.py loaddata data/categories.json
```

### Collect static files
Certain resources, such as CSS and JavaScript files, need to be served from a static directory. Run the following command to collect static files for Django to serve:

```py
python manage.py collectstatic
```

### Create super user
You will need a super user in order to log in and manage CiviWiki:

```py
python manage.py createsuperuser
```

## Run CiviWiki
If the above steps are complete, we can start CiviWiki:

```py
python manage.py runserver
```

## Register initial user
Once CiviWiki is running, visit the front page (probably something like http://localhost:8000). Once there, click 'log in/register', and then 'register new user'.

### Enable beta access for new user
Once you have submitted the new user registration form, you will be directed to the 'Development in progress' screen. In order to access the site functionality, you need to modify the new user record and set the `beta_access` field to `True` for the user record in the `api_account` table.
