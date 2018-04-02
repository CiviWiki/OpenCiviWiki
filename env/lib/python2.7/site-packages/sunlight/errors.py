# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

"""
.. module:: sunlight.errors
    :synopsis: Exceptions and Errors
"""


class SunlightException(Exception):
    """
    :class:`sunlight.errors.SunlightException` is the base exception,
    all other sunlight exceptions (such as
    :class:`sunlight.errors.NoAPIKeyException`) all inherit from this. This
    makes it easy to catch all sunlight errors if you really really need to
    (not that you should)
    """
    def __init__(self, value):
        """
        This is just your basic __init__ method, nothing special here.

        Args:
            value (str): Message to report with the Exception
        """
        self.value = value

    def __str__(self):
        """
        Return the string-ular representation of the exception - this makes it
        super easy to just run something like ``print e`` (given ``e`` is a
        SunlightException instance)
        """
        return repr(self.value)


class BadRequestException(SunlightException):
    """
    This gets thrown when the underlying url request has recieved an abnormal
    response code, or the program has issued a request that can not be filled.
    """
    pass


class InvalidRequestException(BadRequestException):
    """
    This gets thrown when the API gets a valid response, but has an error that
    should be passed back to the program.
    """
    pass


class NoAPIKeyException(SunlightException):
    """
    This gets thrown if the bindings are asked to issue a request, but the
    ``sunlight.config.API_KEY`` variable is ``None``.
    """
    pass
