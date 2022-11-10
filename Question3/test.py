import requests
import json

base = 'https://developers.onemap.sg/'
path = '/commonapi/search'

resp = requests.get(base + path, params={'searchVal': '307987', 'returnGeom': 'Y', 'getAddrDetails': 'N'})
res = resp.json()
s = json.dumps(res, indent=4)
print(s)