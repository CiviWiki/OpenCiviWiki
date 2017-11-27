import sunlight
from django.conf import settings
from sunlight.errors import BadRequestException

def get_legislator_and_district(account):
    location = account.zip_code

    sunlight.config.API_KEY = settings.SUNLIGHT_API_KEY
    district_maps = sunlight.congress.locate_districts_by_zip(location)
    legislator_maps = sunlight.congress.locate_legislators_by_zip(location)

    return dict(districts=district_maps, legislators=legislator_maps)

def get_bill_information(account):
    sunlight.config.API_KEY = settings.SUNLIGHT_API_KEY
    bill_data = []
    preferences = {}
    preferences['state'] = account.state
    # I want to return a max of 50 bills from this function
    preferences['per_page'] = 20 / max(len(account.interests), 1)
    for interest in account.interests:
        preferences['q'] = interest
        bill_data += sunlight.openstates.bills(**preferences)

    return bill_data

def get_legislator_ids_by_lat_long(latitude, longitude):
    """ Gets legislator bioguide_ids by coordinate location"""
    bioguide_ids = []

    try:
        legislators = sunlight.congress.locate_legislators_by_lat_lon(latitude, longitude)
    except BadRequestException:
        return bioguide_ids

    if legislators and len(legislators):
        for legislator in legislators:
            bioguide_ids.append(legislator.get('bioguide_id'))

    return bioguide_ids
