# Contributing

Thank you for your interest in contributing to CiviWiki. There are many ways to contribute, such as by sharing ideas, design, testing, community building, and development.

The following sections outline some common ways to contribue ideas, feature requests, and code.

## Creating issues

Make sure to search beforehand to see if the issue has been previously reported.

The issue tracker should not be used for personal support requests. Please direct those to our [live chat](https://riot.im/app/#/room/#CiviWiki:matrix.org)

### Bug Reports
Please try to have as much detail as possible when creating a bug report.

A good example should contain:

1. A short description of the issue.

2. Detailed description of the bug, including the environment/OS/Browser info if possible.

3. Steps to reproduce the bug.

4. Any identified lines of code involved in the issue or other insight that may help resolve the issue. This can also include any relevant error logs.

5. (Optional)Potential solutions to the problem.

A good bug report will help direct developers to solve the problem at hand without wasting time trying to figure out the problem in the first place.

### Feature requests/enhancements
If you have a budding idea or a feature that requires a more community-involved discussion, consider having the development discussion on the [live chat](https://riot.im/app/#/room/#CiviWiki:matrix.org) or create a thread on [loomio](https://www.loomio.org/g/ET40tXUC/openciviwiki). This will allow for a well-thought-out issue that will more likely be in line with the goal of the project.


## Development

The following sections describe how to set up a development environment. Note, we have tried to simplify our development set-up in order to reduce barriers to entry.

### Install requirements

To install all required modules, complete the following steps:

1. Make sure you are in the repository root directory
2. Create a Python 3.7+ virtual environment (named `env`)
```
python -m venv env
```
3. Activate the virtual environment using:
  * For Windows users:
  ```
  .\env\Scripts\activate
  ```
  * For MacOS and Linux users:
  ```
  source env/bin/activate
  ```
4. Use the following command in project dir:
```
pip install -r requirements/dev.txt
```
5. Change into project directory
```
cd project
```


### Run migrations

To create the (initial) database structure, run migrations as follows:

```py
python manage.py migrate
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


### Populate initial data

During the first setup, it's useful to import hardcoded initial entries. In this case, there are two fixtures:

* Sample threads, located in `project/data/sample_threads.json`
* Sample categories, located in `project/data/categories.json`

Run the following commands to load fixtures:

```py
python manage.py loaddata ./data/categories.json
python manage.py loaddata ./data/sample_threads.json
```

You can also import all of them in one batch:

```py
python manage.py loaddata ./data/*.json
```


### Run the server

Once you have installed the dependencies, run the server as follows:

```py
python manage.py runserver
```

### Run unit tests

Execute unit tests by running the following command from within the `project` directory.

```sh
python manage.py test
```

### Register initial user (optional)
Once CiviWiki is running, visit the front page (probably something like http://localhost:8000). Once there, click 'log in/register', and then 'register new user'.

## Deployment
The [deployment instructions for Heroku](https://github.com/CiviWiki/OpenCiviWiki/wiki/Deployment-instructions-for-Heroku) can be found in the wiki.

## Coding Conventions

We strive to follow Django Coding Conventions. See https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

## Compatible Versioning
We use Compatibile Versioning in this project.

Given a version number MAJOR.MINOR, increment the:

MAJOR version when you make backwards-incompatible updates of any kind
MINOR version when you make 100% backwards-compatible updates
Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR format.

### How is this different to SemVer?

Compatible Versioning ("ComVer") is SemVer where every PATCH number is 0 (zero). This way, ComVer is backwards compatible with SemVer.

A ComVer release from 3.6 to 3.7 is just a SemVer release from 3.6.0 to 3.7.0. In other words, ComVer is safe to adopt since it is basically SemVer without ever issuing PATCH releases.
