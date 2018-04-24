# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.


from sunlight.errors import InvalidRequestException, BadRequestException

import sunlight.service
import json

service_url = "http://capitolwords.org/api/1"


class CapitolWords(sunlight.service.Service):
    """
    Bindings into the `CapitolWords project <http://capitolwords.org>`_.
    Keep in mind, as you use this wrapper, that this is a very thin translation
    layer from the API into Python. There's no object magic, so the docs on the
    API it's self will be as useful as any of these docstrings.

    Feel free to read up on the CapitolWords API in the
    `docs <http://capitolwords.org/api/>`_.

    If a request goes through and gets a normal response code, but the requested
    action is for whatever reason errorful, a
    :class:`sunlight.errors.InvalidRequestException` will be thrown with the
    error string.
    """

    def dates(self, phrase, **kwargs):
        """
        Retrieve information regarding the popularity of a phrase over a
        period of time.

        For a list of optional arguments see `Capitol Words' dates.json
        endpoint <http://capitolwords.org/api/#dates.json>`_.
        """
        kwargs['phrase'] = phrase
        return self.get(["dates"], **kwargs)

    def phrases(self, entity_type, entity_value, **kwargs):
        """
        Retrieve information on the top phrases for an facet.

        A facet can be any date, month, state or legislator.

        For a list of arguments see `Capitol Words' phrases.json
        endpoint <http://capitolwords.org/api/#phrases.json>`_.
        """
        kwargs['entity_type'] = entity_type
        kwargs['entity_value'] = entity_value

        return self.get(["phrases"], **kwargs)

    def phrases_by_entity(self, entity_type, **kwargs):
        """
        Get listing of top facets for a given phrase.

        A facet can be any date, month, state or legislator.

        For a list of arguments see `Capitol Words' phrases/entity.json
        endpoint <http://capitolwords.org/api/#phrases/entity.json>`_.
        """
        return self.get(["phrases", entity_type], **kwargs)

    def text(self, phrase=None, title=None, **kwargs):
        """
        Full text-search against Capitol Words data.

        Neither ``phrase`` nor ``title`` are required, but one or the other
        must be used. If both are omitted, a
        :class:`sunlight.errors.BadRequestException` will be thrown.

        ``phrase`` will do a full-text search on that phrase, whereas
        ``title`` will doa  full-text search on the title of each CR
        (Congressional Record) document.

        For a list of arguments see `Capitol Words' text.json
        endpoint <http://capitolwords.org/api/#text.json>`_.
        """
        if not phrase and not title:
            raise BadRequestException(
                "You must provide one of phrase or title to this method.")

        if phrase:
            kwargs['phrase'] = phrase

        if title:
            kwargs['title'] = title

        return self.get(["text"], **kwargs)

    # API impl methods below

    def _get_url(self, pathparts, apikey, **kwargs):
        # join pieces by slashes and add a trailing slash
        endpoint_path = "/".join(pathparts)

        ret = "%s/%s.json?apikey=%s&%s" % (
            service_url,
            endpoint_path,
            apikey,
            sunlight.service.safe_encode(kwargs)
        )
        return ret

    def _decode_response(self, response):
        ret = json.loads(response)
        if "error" in ret:
            ex = InvalidRequestException(ret['error'])
            ex.response = ret
            raise ex
        if "results" in ret:
            return ret['results']
            # XXX: Verify this is actually
            #      what we want.
        return ret
