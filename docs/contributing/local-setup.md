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
Certain environment variables may be required depending on your local setup. For instance, CiviWiki uses SQLite by default, but you can alternatively set up a PostgreSQL database and provide the necessary environment variables. The following environment variables are optional:

- AWS_STORAGE_BUCKET_NAME
- AWS_S3_ACCESS_KEY_ID
- AWS_S3_SECRET_ACCESS_KEY
- DATABASE_URL
- CIVIWIKI_LOCAL_NAME - database name in local PostgreSQL instance
- CIVIWIKI_LOCAL_USERNAME - username in local PostgreSQL instance with rights to database
- CIVIWIKI_LOCAL_PASSWORD - password for database user

You can save some time and declare those environmental variables all at once with a shell script. E.g.

```sh
#! /bin/bash

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
