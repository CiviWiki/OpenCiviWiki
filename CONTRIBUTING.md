# Set-up instructions
Use these instructions to set up a local development environment.

## Prerequisites
The following packages are helpful/required to start developing CiviWiki:

- PostgreSQL
- Redis
    - [Redis installation instructions](https://redis.io/topics/quickstart)

## Set-up

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

#! /bin/bash

export SUNLIGHT_API_KEY=**********
export GOOGLE_MAP_API_KEY=**********

# PostgreSQL
export CIVIWIKI_LOCAL_NAME=civiwiki
export CIVIWIKI_LOCAL_USERNAME=civiwiki
export CIVIWIKI_LOCAL_PASSWORD=password
```
