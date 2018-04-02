# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

"""
.. module:: sunlight
    :synopsis: Constants and other Globally read things

.. warning::
    If you're using these directly in your app, you might be doing something
    wrong.
"""


API_KEY = None
"""
This might be populated from :func:`sunlight.attempt_to_load_apikey`, or
``None`` (as it is out of the box). All :class:`sunlight.service.Service`
objects will make use of this API key (once, in it's __init__, not after that)
to do their job.

.. note::
    All Sunlight services share API keys. Nice, right?
"""

API_SIGNUP_PAGE = "http://sunlightfoundation.com/api/accounts/register/"
"""
This is a link to the API Key signup page - so that we can sanely direct people
to register for a key (if they don't already have one) -- after all, signing up
for a Sunlight API key is fun for the whole family!
"""

KEY_LOCATION = "~/.sunlight.key"
"""
This is the location of the api key that's stored on the filesystem. Currently,
it uses a file directly under a tilde, so that windows users don't have to feel
as much pain when using the API. Usually this is something like
``~/.sunlight.key``
"""

KEY_ENVVAR = "SUNLIGHT_API_KEY"
"""
This is the name of the ``os.environ`` key to look for. It's usually something
stupid simple, like ``SUNLIGHT_API_KEY``.
"""
