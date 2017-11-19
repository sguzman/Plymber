import requests
import sys
from joblib import Parallel, delayed


cookies = sys.argv[1]
head = {'Cookie': cookies}

url = 'https://partners.uber.com/p3/money/statements/all_data/'
r = requests.get(url, headers=head)
json = r.json()
uuids = [statement['uuid'] for statement in json]
statementTripUrl = 'https://partners.uber.com/p3/money/statements/view/'


def req(uuid):
    j = requests.get(statementTripUrl + uuid, headers=head).json()
    print(uuid, j)
    return j


def trips(js):
    triplist = js['body']['driver']['trip_earnings']['trips'].keys()
    print(triplist)
    return triplist


statements = Parallel(n_jobs=16)(delayed(req)(u) for u in uuids)
tripsList = [trips(j) for j in statements]
tripy = [k for j in tripsList for k in j]

tripUrl = 'https://partners.uber.com/p3/money/trips/trip_data/'


def reqtrip(uuid):
    j = requests.get(tripUrl + uuid, headers=head).json()
    print(uuid, j)
    return j


tripBody = Parallel(n_jobs=32)(delayed(reqtrip)(u) for u in tripy)

print(tripBody)
