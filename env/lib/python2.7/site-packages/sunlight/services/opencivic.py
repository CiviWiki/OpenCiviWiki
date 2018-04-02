# Copyright (c) Sunlight Labs, 2012 under the terms and conditions
# of the LICENSE file.

import sunlight.service
from sunlight.errors import BadRequestException
from sunlight.service import EntityDict
import json

module_name = "opencivic"
service_url = "http://api.opencivicdata.org"


class OpenCivic(sunlight.service.Service):

    def get_list(self, *args, **kwargs):

        def _q(page, *args, **kwargs):
            ret = self.get(*args, page=page, **kwargs)
            page = ret['meta']['page']
            total_pages = ret['meta']['max_page']
            return ret, (page < total_pages)

        page = 0
        if 'page' in kwargs:
            page = kwargs.pop('page')

        has_more = True
        while has_more:
            ret, has_more = _q(page, *args, **kwargs)
            page = ret['meta']['page']
            for entry in ret['results']:
                yield EntityDict(data=entry, meta=ret['meta'])

    def get_object(self, *args, **kwargs):
        ret = self.get(*args, **kwargs)  # In case we get meta eventually.
        return EntityDict(data=ret)

    def jurisdictions(self, **kwargs):
        return self.get_list(["jurisdictions"], **kwargs)

    def divisions(self, **kwargs):
        return self.get_list(["divisions"], **kwargs)

    def organizations(self, **kwargs):
        return self.get_list(["organizations"], **kwargs)

    def people(self, **kwargs):
        return self.get_list(["people"], **kwargs)

    def bills(self, **kwargs):
        return self.get_list(["bills"], **kwargs)

    def votes(self, **kwargs):
        return self.get_list(["votes"], **kwargs)

    def events(self, **kwargs):
        return self.get_list(["events"], **kwargs)

    def info(self, ocd_id, **kwargs):
        return self.get_object([ocd_id], **kwargs)

    def _get_url(self, objs, apikey, **kwargs):
        # Gate for any None's in the query. This is usually a problem.
        if None in objs:
            raise BadRequestException("`None' passed to the URL encoder (%s)" %
                                      (str(objs)))

        # join pieces by slashes and add a trailing slash
        object_path = "/".join(objs)
        object_path += "/"

        return "%s/%s?apikey=%s&%s" % (
            service_url,
            object_path,
            apikey,
            sunlight.service.safe_encode(kwargs)
        )

    def _decode_response(self, response):
        return json.loads(response)
