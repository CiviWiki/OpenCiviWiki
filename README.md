Welcome to Civiwiki!
-------------------

We are an open source, non-profit community, working to develop a democratic engagement web system.

Why CiviWiki?

* **Democratically Contributed Media.** As the name CiviWiki implies, our core content will be contributed by volunteers on our Wiki. Our topic format is modular. The structure both allows a community of volunteers to collaborate on a single political issue, and reserves space for dissenting opinions.
* **Personalized Policy Feed.** CiviWiki intelligently personalizes users' feed in two meaningful ways. First, the issues promoted to users' feed will be personalized to the user's expressed interests, and the timeliness of the issue. Second, the structure of the issue topics break policy positions into bite-sized contentions we call Civies. Each Civi is logically related to the rest of the topic. Based on the user's support, opposition, or neutrality to each Civi, CiviWiki promotes different relevant content.
* **Citizen/Representative Engagement.** CiviWiki's core goal is to engage citizens and their representatives, with the goal of making government more accountable. CiviWiki will achieves this goal in two ways. First, CiviWiki will organize user's policy profile and compare it to every political candidate in the user's district. This quick, detailed, comparison will help users make informed votes, and we believe increased voter confidence will increase voter turnout. Second, CiviWiki will collect anonymized user data and forward district level statistics to representatives. With a critical mass of users, we believe timely district level polling data will influence representatives' votes.

For Developers.
---------------

**NOTE: THIS README IS OUTDATED AND NEEDS TO BE UPDATED ACCORDINGLY**

**Setup**: Setup requires certain environment variables on your machine to be set in order for the application to access secret values, these values are listed below.
* Clone or Fork our repository.
* Create a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).
* `pip install -r requirements.txt`.
* Ensure you have a [database](https://www.postgresql.org/docs/9.1/static/app-createdb.html), and a [user / password](https://www.postgresql.org/docs/9.1/static/app-createuser.html) with [all privileges](https://www.postgresql.org/docs/9.0/static/sql-grant.html), the app will look for this connection using credentials stored in enviornment variables, you can get more details on this below.
* It is required when running `python manage.py <function>` that you explicitly state what settings module you are using.
  * Use `--settings=civiwiki.settings.local` to run the application with your local database credentials.
  * Use `--settings=civiwiki.settings.dev` to run the application on a development server you have hosted.
  * Use `--settings=civiwiki.settings.production` to run the application on a production server. **WARNING: Debug is False**.
  
Versioning System 
  Semantic Versioning Summary 
Given a version number MAJOR.MINOR.PATCH, increment the:

MAJOR version when you make incompatible API changes,
MINOR version when you add functionality in a backwards-compatible manner, and
PATCH version when you make backwards-compatible bug fixes.
Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

 Semantic Versioning Specifications
The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Software using Semantic Versioning MUST declare a public API. This API could be declared in the code itself or exist strictly in documentation. However it is done, it should be precise and comprehensive.

A normal version number MUST take the form X.Y.Z where X, Y, and Z are non-negative integers, and MUST NOT contain leading zeroes. X is the major version, Y is the minor version, and Z is the patch version. Each element MUST increase numerically. For instance: 1.9.0 -> 1.10.0 -> 1.11.0.

Once a versioned package has been released, the contents of that version MUST NOT be modified. Any modifications MUST be released as a new version.

Major version zero (0.y.z) is for initial development. Anything may change at any time. The public API should not be considered stable.

Version 1.0.0 defines the public API. The way in which the version number is incremented after this release is dependent on this public API and how it changes.

Patch version Z (x.y.Z | x > 0) MUST be incremented if only backwards compatible bug fixes are introduced. A bug fix is defined as an internal change that fixes incorrect behavior.

Minor version Y (x.Y.z | x > 0) MUST be incremented if new, backwards compatible functionality is introduced to the public API. It MUST be incremented if any public API functionality is marked as deprecated. It MAY be incremented if substantial new functionality or improvements are introduced within the private code. It MAY include patch level changes. Patch version MUST be reset to 0 when minor version is incremented.

Major version X (X.y.z | X > 0) MUST be incremented if any backwards incompatible changes are introduced to the public API. It MAY include minor and patch level changes. Patch and minor version MUST be reset to 0 when major version is incremented.

A pre-release version MAY be denoted by appending a hyphen and a series of dot separated identifiers immediately following the patch version. Identifiers MUST comprise only ASCII alphanumerics and hyphen [0-9A-Za-z-]. Identifiers MUST NOT be empty. Numeric identifiers MUST NOT include leading zeroes. Pre-release versions have a lower precedence than the associated normal version. A pre-release version indicates that the version is unstable and might not satisfy the intended compatibility requirements as denoted by its associated normal version. Examples: 1.0.0-alpha, 1.0.0-alpha.1, 1.0.0-0.3.7, 1.0.0-x.7.z.92.

Build metadata MAY be denoted by appending a plus sign and a series of dot separated identifiers immediately following the patch or pre-release version. Identifiers MUST comprise only ASCII alphanumerics and hyphen [0-9A-Za-z-]. Identifiers MUST NOT be empty. Build metadata SHOULD be ignored when determining version precedence. Thus two versions that differ only in the build metadata, have the same precedence. Examples: 1.0.0-alpha+001, 1.0.0+20130313144700, 1.0.0-beta+exp.sha.5114f85.

Precedence refers to how versions are compared to each other when ordered. Precedence MUST be calculated by separating the version into major, minor, patch and pre-release identifiers in that order (Build metadata does not figure into precedence). Precedence is determined by the first difference when comparing each of these identifiers from left to right as follows: Major, minor, and patch versions are always compared numerically. Example: 1.0.0 < 2.0.0 < 2.1.0 < 2.1.1. When major, minor, and patch are equal, a pre-release version has lower precedence than a normal version. Example: 1.0.0-alpha < 1.0.0. Precedence for two pre-release versions with the same major, minor, and patch version MUST be determined by comparing each dot separated identifier from left to right until a difference is found as follows: identifiers consisting of only digits are compared numerically and identifiers with letters or hyphens are compared lexically in ASCII sort order. Numeric identifiers always have lower precedence than non-numeric identifiers. A larger set of pre-release fields has a higher precedence than a smaller set, if all of the preceding identifiers are equal. Example: 1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0.

Environment Variables

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
