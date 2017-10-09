[![ComVer](https://img.shields.io/badge/ComVer-compliant-brightgreen.svg)](https://github.com/staltz/comver)
[![Stories in Ready](https://badge.waffle.io/CiviWiki/OpenCiviWiki.png?label=ready&title=Ready)](https://waffle.io/CiviWiki/OpenCiviWiki?utm_source=badge)

# Welcome to Civiwiki!

We are an open source, non-profit community, working to develop a democratic engagement web system.

## Why CiviWiki?

* **Democratically Contributed Media.** As the name CiviWiki implies, our core content will be contributed by volunteers on our Wiki. Our topic format is modular. The structure allows both a community of volunteers to collaborate on a single political issue, and reserves space for dissenting opinions.
* **Personalized Policy Feed.** CiviWiki intelligently personalizes users' feed in two meaningful ways. First, the issues promoted to users' feed will be personalized to the user's expressed interests, and the timeliness of the issue. Second, the structure of the issue topics break policy positions into bite-sized contentions we call Civies. Each Civi is logically related to the rest of the topic. Based on the user's support, opposition, or neutrality to each Civi, CiviWiki promotes different relevant content.
* **Citizen/Representative Engagement.** CiviWiki's core goal is to engage citizens and their representatives, with the goal of making government more accountable. CiviWiki will achieve this goal in two ways. First, CiviWiki will organize user's policy profile and compare it to every political candidate in the user's district. This quick, detailed, comparison will help users make informed votes, and we believe increased voter confidence will increase voter turnout. Second, CiviWiki will collect anonymized user data and forward district level statistics to representatives. With a critical mass of users, we believe timely district level polling data will influence representatives' votes.
  

# Development
## Compatible Versioning
We use Compatibile Versioning in this project.

Given a version number MAJOR.MINOR, increment the:

MAJOR version when you make backwards-incompatible updates of any kind
MINOR version when you make 100% backwards-compatible updates
Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR format.

### How is this different to SemVer?

Compatible Versioning ("ComVer") is SemVer where every PATCH number is 0 (zero). This way, ComVer is backwards compatible with SemVer.

A ComVer release from 3.6 to 3.7 is just a SemVer release from 3.6.0 to 3.7.0. In other words, ComVer is safe to adopt since it is basically SemVer without ever issuing PATCH releases.

## Coding Conventions 

We strive to follow Django Coding Conventions. See https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

## Development environment
### setup

1. Clone or Fork our repository.
2. Create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
3. Activate the virtual environment
4.  `pip install -r requirements.txt`.
5. Ensure you have a [database](https://www.postgresql.org/docs/9.1/static/app-createdb.html), and a [user / password](https://www.postgresql.org/docs/9.1/static/app-createuser.html) with [all privileges](https://www.postgresql.org/docs/9.0/static/sql-grant.html), the app will look for this connection using credentials stored in enviornment variables, you can get more details on this below.

It is required when running `python manage.py <function>` that you explicitly state what settings module you are using.
* Use `--settings=civiwiki.settings.local` to run the application with your local database credentials.
* Use `--settings=civiwiki.settings.dev` to run the application on a development server you have hosted.
* Use `--settings=civiwiki.settings.production` to run the application on a production server. **WARNING: Debug is False**.

### Environment Variables

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

# Contribute
Contact us on Twitter to join the team.

I want to keep track of how Civiwiki is doing.

# Contact info

* **Twitter:** [@CiviWiki](https://twitter.com/civiwiki)
