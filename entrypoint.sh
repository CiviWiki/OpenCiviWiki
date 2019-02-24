#!/bin/sh

localserver()
{
    sleep 10
    python /app/project/manage.py migrate
    python /app/project/manage.py runserver 0.0.0.0:8000
}

for cmd in $@
do
   $cmd
done
