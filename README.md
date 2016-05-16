Welcome to Civiwiki!
-------------------

We are a non-profit community working to develop a democratic engagement web system.

Why CiviWiki?

* **Democratically Contributed Media.** As the name CiviWiki implies, our core content will be contributed by volunteers on our Wiki. Our topic format is modular. The structure both allows a community of volunteers to collaborate on a single political issue, and reserves space for dissenting opinions.
* **Personalized Policy Feed.** CiviWiki intelligently personalizes users' feed in two meaningful ways. First, the issues promoted to users' feed will be personalized to the user's expressed interests, and the timeliness of the issue. Second, the structure of the issue topics break policy positions into bite-sized contentions we call Civies. Each Civi is logically related to the rest of the topic. Based on the user's support, opposition, or neutrality to each Civi, CiviWiki promotes different relevant content.
* **Citizen/Representative Engagement.** CiviWiki's core goal is to engage citizens and their representatives, with the goal of making government more accountable. CiviWiki will achieves this goal in two ways. First, CiviWiki will organize user's policy profile and compare it to every political candidate in the user's district. This quick, detailed, comparison will help users make informed votes, and we believe increased voter confidence will increase voter turnout. Second, CiviWiki will collect anonymized user data and forward district level statistics to representatives. With a critical mass of users, we believe timely district level polling data will influence representatives' votes.

For Developers.
---------------

**Setup**: Setup requires certain environment variables on your machine to be set in order for the application to access secret values, these values are listed below.
* Clone or Fork our repository.
* Create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
* `pip install -r requirements.txt`.
* It is required when running `python manage.py <function>` that you explicitly state what settings module you are using.
  * Use `--settings=civiwiki.settings.local` to run the application with your local database credentials.
  * Use `--settings=civiwiki.settings.dev` to run the application on a development server you have hosted.
  * Use `--settings=civiwiki.settings.production` to run the application on a production server. **WARNING: Debug is False**.

**Below is a list of environment variables expected to be present when you run your server.** The application does not manage how you keep track of these variables ( a recommended [solution](http://stackoverflow.com/a/11134336) ) and only checks for variables that are needed at the time. For example, production database environment variables do not need to be present if developing locally.
* **DJANGO_SECRET_KEY**: _This value **must** be in the list of environment variables._ Information on the Django Secret Key can be found [here](https://docs.djangoproject.com/en/1.8/ref/settings/#secret-key), information on generating a key can be found in this StackOverflow [post](http://stackoverflow.com/questions/4664724/distributing-django-projects-with-unique-secret-keys/16630719#16630719).
* **SUNLIGHT_API_KEY**: _This value **must** be in the list of environment variables._ Information on retrieving a [Sunlight API](https://sunlightfoundation.com/api) Key can be found [here](https://sunlightfoundation.com/api/accounts/register/).
* **CIVIWIKI_LOCAL_NAME:** name of database to be used when searching your localhost databases.
* **CIVIWIKI_LOCAL_USERNAME:** username the application should use to access your localhost database.
* **CIVWIKI_LOCAL_PASSWORD:** password the user needs to log into your localhost database.
* **CIVIWIKI_DEV_HOST:** address where development database is hosted.
* **CIVIWIKI_DEV_PORT:** port number to access database to _(5432 if unsure)_.
* **CIVIWIKI_DEV_NAME:** name of database to be used when accessing databases on your server.
* **CIVIWIKI_DEV_ENGINE:** set to _django.db.backends.postgresql_psycopg2_.
* **CIVIWKIKI_DEV_USERNAME:** username that application should use to access your localhost database.
* **CIVIWIKI_DEV_PASSWORD:** password the user needs to log into your localhost database.

_Production settings are configured to be run on an Amazon AWS Instance connecting to their RDS services._



**Contribute**:
Contact us on Twitter to join the team.

I want to keep track of how Civiwiki is doing.
----------------------------------------------

#### Contact info

* **Twitter:** [@CiviWiki](https://twitter.com/civiwiki)
* **Web:** http://civiwiki.launchrock.com/
