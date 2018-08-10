import Model from model

def get_legislator_and_district(account):
    """
    Given the ZIP code, and latitude/longitude of the account, it pulls the state,
    the district, and the legislators from both the house, and the senate.
    """
    #This first sanity checks the zip, then makes sure it is in the USA.  If yes, continue.
    #This tries to pull from our local database, and failing that, from Propublica.
    
    sleg_list = []
    rleg_list = []

    if (((account.zip_code) < 10000)||((account.zip_code) > 100000)):
        #Get zip and ward from Lat/Long?
            #yeah, we will save that for later, it is crazy difficult right now
            #For now, throw Bad Zip error.
        throw BadZipCodeException #custom error this
    else:  #valid zip
        #get state, and district, then get congresscritter for ward/district
        
        #Senator is just the state, House is the hard one
        sleg_list = MembersClient.filter("senate", CURRENT_CONGRESS, account.state)
        rleg_list = MembersClient.filter("house", CURRENT_CONGRESS, account.state, account.district)
        #Still need to get district from location
        
    #Getting it from the ProPublica page works while we are small, but there is a limit
    #of 5000 requests per day, so we need to download, and store the info locally
    #update it once per day
    return (sleg_list, rleg_list, district)
    

    
#duplicate of getLegislators(account) in account.js?
#def get_legislator_ids_by_lat_long(latitude, longitude):
#    """
#    Gets IDs by latitude and longitude.
#    Pulls from stored location first, if that is empty, pull from ProPublica
#    """
#    leg_list = []
#
#    try:
#        legislators =
#        except BadRequestException:
#            return leg_list
