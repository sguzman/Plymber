import requests
import sys
from joblib import Parallel, delayed
import uber


cookies = ''
if len(sys.argv) is 2:
    cookies = sys.argv[1]
else:
    cookiesDict = uber.cookie()
    cookies = '; '.join(['{}={}'.format(x, cookiesDict[x]) for x in cookiesDict.keys()])


head = {'Cookie': cookies}

url = 'https://partners.uber.com/p3/money/statements/all_data/'
r = requests.get(url, headers=head)
json = r.json()
uuids = [statement['uuid'] for statement in json]
statementTripUrl = 'https://partners.uber.com/p3/money/statements/view/'


def req(uuid):
    print('Processing statement uuid', uuid)
    j = requests.get(statementTripUrl + uuid, headers=head).json()
    return j


def trips(js):
    triplist = list(js['body']['driver']['trip_earnings']['trips'].keys())
    print('Extracted trip uuid list', triplist)
    return triplist


statements = Parallel(n_jobs=16, backend='threading')(delayed(req)(u) for u in uuids)
tripsList = [trips(j) for j in statements]
tripy = [k for j in tripsList for k in j]

tripUrl = 'https://partners.uber.com/p3/money/trips/trip_data/'


def reqtrip(uuid):
    print('Processing trip uuid', uuid)
    j = requests.get(tripUrl + uuid, headers=head).json()
    return j


tripBody = Parallel(n_jobs=32, backend='threading')(delayed(reqtrip)(u) for u in tripy)

print(tripBody)
