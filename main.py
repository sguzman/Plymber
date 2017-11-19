import requests
import sys


#cookies = uber.cookie()

cookies = sys.argv[1]

url = 'https://partners.uber.com/p3/money/statements/all_data/'
r = requests.get(url, headers={'Cookie': cookies})


print(r.json())