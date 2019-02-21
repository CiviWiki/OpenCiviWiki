#!/bin/sh

localserver()
{
    sleep 10
    xvfb-run java -Dwebdriver.chrome.driver=/usr/bin/chromedriver -jar /usr/selenium-server-standalone.jar &
    chromedriver --url-base=/wd/hub --whitelisted-ips="" &

    python /app/project/manage.py migrate
    python /app/project/manage.py runserver 0.0.0.0:8000
}

for cmd in $@
do
   $cmd
done
