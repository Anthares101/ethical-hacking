# Python 3 requirements: json
#
# A little auxiliary script for domains_to_assets.py output, will read the JSON and return a pretty print of it.

import json
import collections
import re

from tabulate import tabulate


with open('public_assets.json') as assets_file:
	assets = json.load(assets_file)

# Parse JSON
parsed_dict = collections.defaultdict(list)
for asset in assets.keys():
	# Get only the IPs for domains
	ips_and_domains = asset.split(',')
	ips = ''
	for ip_or_domain in ips_and_domains:
		if not re.search('[a-zA-Z]', ip_or_domain):
			if ips:
				ips = ips + ','
			ips = ips + ip_or_domain

	# Order by TLD
	domains = assets[asset]
	for domain in domains:
		tld = '.'.join(domain.split('.')[-2:])
		parsed_dict[tld].append([domain, ips])

# Pretty print
for tld in parsed_dict.keys():
	domains_and_ips = parsed_dict[tld]
	print(tabulate(domains_and_ips, headers=[tld], tablefmt='fancy_grid'))
	print()
