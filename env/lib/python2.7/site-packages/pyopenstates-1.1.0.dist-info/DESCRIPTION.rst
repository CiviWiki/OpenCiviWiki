pyopenstates
============

|Build Status|

A Python client for the `Open States API`_.

The `Open States`_ project provides data on legislators, bills,
committees, and districts in legislatures of all 50 US states, plus D.C.
and Puerto Rico. This data is gathered directly from the legislatures,
and converted to a common format for interested developers, through a
JSON API and data dumps. The project was originally created by the
`Sunlight Foundation`_ as a part of Sunlight Labs. The Sunlight
Foundation has since `shut down`_ Sunlight Labs, and Open States is now
an `independent project`_.

This module is intended to be a replacement for the ``openstates``
methods provided by the origional ``sunlight`` package. However, it is
not a drop-in replacement; the methods are slightly different, and some
features have been added.

Please consider `donating`_ or `volunteering`_ to support the Open
States project. The data provided to the public by various legislatures
can frequently change format. Without regularly-maintained scrapers and
server infrastructure, this consistent and free API would not be
possible.

Features
--------

-  Compatible with Python 2.7-3+
-  Full Unicode support
-  Supports all methods, options, and data types provided by the API
-  Methods for downloading data dumps
-  Automatic conversion of string dates and timestamps to ``datetime``
   objects
-  Tested releases
-  Set API Key via environment variable or in code.

Installation
------------

``pyopenstates`` can be installed using `pip`_.
Installation in a `virtualenv`_ is recommended.


To install the latest release, run:

::

    $ pip install -U pyopenstates

Or, install the latest commit from git, run:

::

    $ pip install -U git+https://github.com/openstates/pyopenstates

API Keys
--------

To use the Open States API you must `obtain an API Key`_.

Once you have your key you can use it with this library by setting the ``OPENSTATES_API_KEY`` environment variable or calling ``pyopenstates.set_api_key``.

Documentation
-------------

Documentation is provided in detailed docstrings, and in HTML format at

https://openstates.github.io/pyopenstates/

.. _Open States API: http://docs.openstates.org/api/
.. _Open States: https://openstates.org/
.. _Sunlight Foundation: https://sunlightfoundation.com/
.. _shut down: https://sunlightfoundation.com/2016/09/21/whats-next-for-sunlight-labs/
.. _independent project: https://blog.openstates.org/post/adopting-open-states/
.. _donating: https://www.generosity.com/fundraising/open-states-general-support-fund
.. _volunteering: https://docs.google.com/forms/d/e/1FAIpQLSfMDjoVoKxSOciIiqE3Ofxgn-caFGCxicFO2LwyWAK8zdXyhg/viewform
.. _pip: https://docs.python.org/3.5/installing/index.html
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _obtain an API Key: https://openstates.org/api/register/

.. |Build Status| image:: https://travis-ci.org/openstates/pyopenstates.svg?branch=master
   :target: https://travis-ci.org/openstates/pyopenstates


