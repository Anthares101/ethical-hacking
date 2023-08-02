# Python 3 requirements: json
#
# A little auxiliary script for domains_to_assets.py output, will read the JSON and return just a list of domains.

import json


with open('public_assets.json') as assets_file:
	assets = json.load(assets_file)

for asset in assets.keys():
	domains = assets[asset]
	for domain in domains:
		print(domain)
