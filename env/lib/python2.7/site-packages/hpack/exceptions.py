# -*- coding: utf-8 -*-
"""
hyper/http20/exceptions
~~~~~~~~~~~~~~~~~~~~~~~

This defines exceptions used in the HTTP/2 portion of hyper.
"""


class HPACKError(Exception):
    """
    The base class for all ``hpack`` exceptions.
    """
    pass


class HPACKDecodingError(HPACKError):
    """
    An error has been encountered while performing HPACK decoding.
    """
    pass


class InvalidTableIndex(HPACKDecodingError):
    """
    An invalid table index was received.
    """
    pass


class OversizedHeaderListError(HPACKDecodingError):
    """
    A header list that was larger than we allow has been received. This may be
    a DoS attack.

    .. versionadded:: 2.3.0
    """
    pass
