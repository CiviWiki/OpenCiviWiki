"""
The base class from which all ProPublica and OpenSecrets functions derive their power,
from the base client to interacting with theirrespective APIs and/or django databases.
"""

import .json
import .logging
import .httplib2
#this goes with the congresscritters class
from django.db import models

class PClient(object):
    """
    PClient deals with fetching responses from eith the ProPublica API, or the OpenSecrets API
    , and dealing with what is returned.

    The httplib2 stuff is shamelessly stolen from StackOverflow
    """

    BASE_URI = "https://api.propublica.org/congress/v1"
    #Gonna have to move this, and add Open Secrets URI

    def __init__(self, apikey=None, cache='.cache', http=None):
        self.apikey = apikey

        if isinstance(http, httplib2.Http):
            self.http = http
        else:
            self.http = httpli2.Http(cache)

    def fetch(self, path, parse=lambda r: r['results'][0]):
        """
        Makes the API request, WITH auth.
        """

        url = self.BASE_URL + path
        headers = {'X-API-Key': self.apikey}
        log.debug(url)
        resp, content = self.http.request(url, headers=headers)
        content = u(content)
        content = json.loads(content)

        #Error handling
        if not content.get('status') == 'OK':
            if content.get('status') == '404':
                raise NotFound(path)
            if "errors" in content and content['errors'][0]['error'] == "Record not Found":
                raise NotFound(path)
            raise CongressError(content, resp, url)

        if callable(parse):
            content = parse(content)

        return content


class CongresscritterDB(Models.model):
    def __init__():
        #Check to see if DB exists
        #check to see how old DB is, if > 1 day, pull data
        #possible to compare, then pull only deltas?  Probably not.
        pass
    
    def makeDB(self, apikey, chamber):#finish
        pass

    def updateDB(self, apikey, chamber):
        pass
    
