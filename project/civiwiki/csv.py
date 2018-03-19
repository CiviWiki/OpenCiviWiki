from datetime import datetime
import csv

#Keeps a one minute cooldown between pulls, to slow a bad actor.
def CSV_lookup(username, time, thread):
    #open file that holds list of unames, times
    #compare times, if < 1 min, return error message
    #if > 1 min, overwrite time with new one, goto csv function
    dicts_from_file = []
    with open(CSVNamesandTimes.dat, r) as f:
        for line in f:
            dicts_from_file.append(eval(line))
    if(for k, v in dicts_from_file):
        if(k == username):
            if((datetime.utcnow - v) < 60): #confirm 60 is correct
                return "Dowloading CSVs too quickly, please wait one minute\n"
            else:
                CSV_creator(username, thread)
                        ;
    else: #username not in file
        dicts_from_file.append(username, datetime.utcnow())

    with open(CSVNamesandTimes.dat, w) as f:
        for k,v in dicts_from_file:
            f.write(str(k) + ' >>> ' + str(v) + '\n\n')

#CSV Parser.  Any registered user can pull any civi as a csv
def CSV_creator(username, thread):
    
    #File will be named CiviWiki<TIME>.csv
    #Time is ISO 8601 format:  YYYY-MM-DDTHH:MM:SSZ
    #Z means UTC time, in J2000 epoch
    A = {0}{1}{2}.format("OpenCiviWiki", datetime.utcnow().strftime("%Y-%m-%d%H:%M:%S"), ".csv")

    open(A, "wb") as csvfile:
        ;
