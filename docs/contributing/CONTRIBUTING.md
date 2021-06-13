# Creating Issues

Make sure to search beforehand to see if the issue has been previously reported.

The issue tracker should not be used for personal support requests. Please direct those to our [live chat](https://discord.gg/zkAe55bEkh)

## Bug Reports
Please try to have as much detail as possible when creating a bug report.

A good example should contain:

1. A short description of the issue.

2. Detailed description of the bug, including the environment/OS/Browser info if possible.

3. Steps to reproduce the bug.

4. Any identified lines of code involved in the issue or other insight that may help resolve the issue. This can also include any relevant error logs.

5. (Optional)Potential solutions to the problem.

A good bug report will help direct developers to solve the problem at hand without wasting time trying to figure out the problem in the first place.

## Feature Requests/Enhancements
If you have a budding idea or a feature that requires a more community-involved discussion, consider having the development discussion on the [live chat](https://discord.gg/zkAe55bEkh) or create a thread on [loomio](https://www.loomio.org/g/ET40tXUC/openciviwiki). This will allow for a well-thought-out issue that will more likely be in line with the goal of the project.

# Set-up instructions
Use instruction from one of points below:

* [Docker setup](docker-setup.md)
* [Local setup](local-setup.md)

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

# Deployment
The [deployment instructions for Heroku](https://github.com/CiviWiki/OpenCiviWiki/wiki/Deployment-instructions-for-Heroku) can be found in the wiki.

# Coding Conventions

We strive to follow Django Coding Conventions. See https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

# Compatible Versioning
We use Compatibile Versioning in this project.

Given a version number MAJOR.MINOR, increment the:

MAJOR version when you make backwards-incompatible updates of any kind
MINOR version when you make 100% backwards-compatible updates
Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR format.

## How is this different to SemVer?

Compatible Versioning ("ComVer") is SemVer where every PATCH number is 0 (zero). This way, ComVer is backwards compatible with SemVer.

A ComVer release from 3.6 to 3.7 is just a SemVer release from 3.6.0 to 3.7.0. In other words, ComVer is safe to adopt since it is basically SemVer without ever issuing PATCH releases.
