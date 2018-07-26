import Model from model

def get_legislator_and_district(account):
    """
    This first sanity checks the zip, then makes sure it is in the USA.  If yes, continue.
    This tries to pull from our local database, and failing that, from Propublica.
    """
    
    location = account.zip_code

    if ((location < 10000)||(location > 100000)):
        throw BadRequestException #custom error this
    else:  #valid zip
        #get state, and ward, then get congresscritter for ward
        

    #Getting it from the ProPublica page works while we are small, but there is a limit
    #of 5000 requests per day, so we need to download, and store the info locally
    #update it once per day

    

    return NULL;

def get_legislator_ids_by_lat_long(latitude, longitude):
    """
    Gets IDs by lat, long.
    Pulls from stored location first, if that is empty, pull from ProPublica
    """
    leg_list = []

    try:
        legislators =
        except BadRequestException:
            return leg_list
