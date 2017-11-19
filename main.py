import requests
import sys
import multiprocessing
from joblib import Parallel, delayed


cookies = sys.argv[1]
head = {'Cookie': cookies}

url = 'https://partners.uber.com/p3/money/statements/all_data/'
r = requests.get(url, headers=head)
json = r.json()
uuids = [statement['uuid'] for statement in json]
statementTripUrl = 'https://partners.uber.com/p3/money/statements/view/'

numCores = multiprocessing.cpu_count()


def req(uuid):
    j = requests.get(statementTripUrl + uuid, headers=head).json()
    print(uuid, j)
    return j


statements = Parallel(n_jobs=16)(delayed(req)(u) for u in uuids)

print(statements)
