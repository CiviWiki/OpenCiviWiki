[![Stories in Ready](https://badge.waffle.io/CiviWiki/OpenCiviWiki.png?label=ready&title=Ready)](https://waffle.io/CiviWiki/OpenCiviWiki?utm_source=badge)
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
  
Compatible Versioning

Summary

Given a version number MAJOR.MINOR, increment the:

MAJOR version when you make backwards-incompatible updates of any kind
MINOR version when you make 100% backwards-compatible updates
Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR format.

Use the badge in your library:

ComVer

[![ComVer](https://img.shields.io/badge/ComVer-compliant-brightgreen.svg)](https://github.com/staltz/comver)
How is this different to SemVer?

Compatible Versioning ("ComVer") is SemVer where every PATCH number is 0 (zero). This way, ComVer is backwards compatible with SemVer.

A ComVer release from 3.6 to 3.7 is just a SemVer release from 3.6.0 to 3.7.0. In other words, ComVer is safe to adopt since it is basically SemVer without ever issuing PATCH releases.

Why Use Compatible Versioning?

After the introduction of SemVer, meant to solve "dependency hell", we still experience severe dependency update issues. In part, we don't fully understand and follow SemVer, in part, SemVer is problematic and allows package authors to use their own personal judgement. Either way, those problems are consequence of SemVer itself: it is not easily understood and it allows personal judgement.

In SemVer:

MAJOR is for backwards-incompatible updates
MINOR is for backwards-compatible features
PATCH is for backwards-compatible bug fixes
SemVer gives special treatment for bug fixes. This is problematic because it is often debatable whether a software behavior is a bug or a feature, as is commonly known among developers. There are many cases where package authors should have issued a MAJOR update for a backwards-incompatible bug fix, but since PATCH is commonly used for bug fixes, they update PATCH. This may happen because they have no ways of checking whether people rely on the buggy behavior "as a feature". If no one relies on the buggy behavior as a feature, then it is safe to update PATCH. If not, then the most appropriate choice would have been MAJOR.

It is possible to avoid making personal judgements by using automated tools such as semantic-release that follow SemVer strictly. However, such tools rely on the fact the test coverage for the package is extensive, in order to detect corner cases.

While it is possible to interpret SemVer strictly, SemVer actually advises package authors to "use their best judgement" considering the audience impact of their packages. Even if well intentioned and well informed, package authors will have different judgements of what updates deserves a MAJOR or PATCH increment. In any large-scale package manager, this will lead to irregular decisions.

These problems stem from the fact that SemVer requires answering two questions when releasing a new version:

Is it backwards-compatible or not?
Is it a feature or a bug fix?
The mere fact of having to answer two questions for one release leads to problems, specially since one of those questions is subjective. There is a human tendency of preferring not to increment the MAJOR number, which influences the answer to the second question. Only answers to the first question are non-arguable, computable and reliable. That is how semantic-release works, by detecting the presence of backwards-incompatible changes only. To answer the second question, it relies on a human having indicated feature vs bugfix in a commit message.

In ComVer you only need to answer the first question. The answer is 'yes'/'no', where 'yes' means incrementing the MINOR number, and 'no' means incrementing the MAJOR number. Any mistakes in answering this question can be argued in a technical manner, without involving any human judgement. There will never be a debate whether some version update followed ComVer or not.

What about communicating big new releases or new features?

Software versions have typically used the MAJOR number for communicating large overhauls such as "2.0". Versions with new features have typically used the MINOR number for communicating new backwards-compatible features, like in SemVer. With ComVer, both bug fixes and features can be released under MINOR.

That may lift a concern that ComVer is less semantic than SemVer in communicating those changes. However, when managing a set of dependencies in a codebase, the most important question is about Compatibility. Developers are concerned in updating packages while not breaking existing code. A MINOR update in SemVer would communicate "this version has new features" but the developer cannot know, from the version number alone, which features those are. The developer must read the CHANGELOG or Release notes in order to discover the new feature. Similarly with MAJOR updates in SemVer, the developer also needs to read Release notes and migration guides.

ComVer is semantic in the sense that it communicates only one concern: is it compatible? A MAJOR ComVer update means it is backwards-incompatible and reading the release notes is required. A MINOR ComVer update means it is backwards-compatible and there is no need to read any release notes. Maintaining compatibility is the most important concern when updating dependencies in a codebase. New features are "nice to have" and anyway require reading release notes.

Hence we recommend communicating new features in the Release notes, as well as how to use the new features. Communicating big new releases such as overhauls can be done in "human-friendly" ways such as with code names. Ubuntu versions have traditionally used animals and adjectives as code names. Other software, such as VSCodeVim and Om, have used code names for important versions too.

As far as ComVer is concerned, it is strict, always verifiable, non-human, and only concerns backward compatibility.

How to communicate breaking changes?

Most breaking changes are tiny differences in behavior caused by bug fixes. They are normally safe for the majority of users to migrate. Other breaking changes affect the API in a minor way. Yet other breaking changes are truly part of an overhaul and require all users to carefully migrate their code.

There is naturally different degrees of importance for breaking changes. To communicate changes, always use a changelog or release notes. To communicate importance of the breaking change in your release notes, we recommend the following changes that answer an fundamental question from your library users: "will (upgrading) affect me (requiring manual migration)?"

You can answer that question with a badge that makes it easy to glance:

yes

![yes](https://img.shields.io/badge/will%20it%20affect%20me%3F-yes-red.svg)
probably will

![probably will](https://img.shields.io/badge/will%20it%20affect%20me%3F-probably%20will-orange.svg)
maybe will

![maybe will](https://img.shields.io/badge/will%20it%20affect%20me%3F-maybe%20will-yellow.svg)
maybe won't

![maybe won't](https://img.shields.io/badge/will%20it%20affect%20me%3F-maybe%20won't-yellowgreen.svg)
probably won't

![probably won't](https://img.shields.io/badge/will%20it%20affect%20me%3F-probably%20won't-green.svg)
no

![no](https://img.shields.io/badge/will%20it%20affect%20me%3F-no-brightgreen.svg)
The last, "will it affect me? no" is only for MINOR versions. All others are for MAJOR versions. These badges reflect the library author's own personal judgement of how much will the change affect the users. However, there should always be accurate descriptions of what changed and how to migrate in case the library user is affected by the change.

Compatible Versioning Specification (ComVer)

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Software using Compatible Versioning MUST declare a public API. This API could be declared in the code itself or exist strictly in documentation. However it is done, it should be precise and comprehensive.
A new software version is said to be "backwards compatible" with a previous version if the new version supports all the use cases of the previous version, with no observable effect on the behavior of the software. The new version MAY support new use cases, but MUST support all the use cases of the previous in order to be backwards compatible. The API defines the "use cases", and the "behavior" of the software includes both features and bugs.
A normal version number MUST either take the form X.Y.0 or the form X.Y. It SHOULD take the form X.Y.0 but MAY take the form X.Y. The numbers X and Y are non-negative integers, and MUST NOT contain leading zeroes. X is the major version and Y is the minor version. Each element MUST increase numerically. For instance: 1.9 -> 1.10 -> 1.11. If the version number takes the form X.Y.0, the zero at the end is called the "patch" version.
Once a versioned package has been released, the contents of that version MUST NOT be modified. Any modifications MUST be released as a new version.
Zero for major version (0.Y.0) MAY be used, it does not differ anyhow from other major version numbers. The same rules apply to both major version zero and major version positive integer.
Minor version Y (x.Y.0) MUST be incremented if new software is released while being backwards compatible. The new software MAY include bug fixes or new features or any other change, as long as the behaviors of previous use cases are preserved.
Major version X (X.y.0) MUST be incremented if any backwards incompatible changes are introduced to the behavior of the software. It MAY include minor level changes. Minor version MUST be reset to 0 when major version is incremented.
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
