# Python 3 requirements: IPy, progressbar2
# Apt requirements: dnsutils
#
# Just something to resolve all domains and subdomains found during the discovery phase and have the results in a fancy JSON format. The script
# also splits domains into domains only available in the internal network and public ones (Domains with no records are filtered out).

import json, subprocess, progressbar, sys, argparse
from IPy import IP


parser = argparse.ArgumentParser(
	description='Get all your discovered domains/subdomains resolved and properly structured. Domains with no records are filtered out.'
)
parser.add_argument('-if', '--input-file', type=str, help='file containing all the domains and subdomains (One per line)', required=True)
parser.add_argument('--public-assets-file', type=str, help='output file containing all public assets', default='public_assets.json')
parser.add_argument('--private-assets-file', type=str, help='output file containing all private assets', default='private_assets.json')

args = parser.parse_args()
input_file = args.input_file
public_assets_file = args.public_assets_file
private_assets_file = args.private_assets_file

print('Resolving all domains provided...', file=sys.stderr)
with open(input_file) as domains_file:
	file_lines = domains_file.readlines()

resolved_domains = []
for file_line in progressbar.progressbar(file_lines):
	dig_result = subprocess.run(['/usr/bin/dig', '+short', file_line.strip()], stdout=subprocess.PIPE)
	if(dig_result.stdout):
		dig_result_list = dig_result.stdout.decode().strip().split('\n')
		dig_result_list.sort()

		resolved_domains.append(
			file_line.strip() + '-->' + ','.join(dig_result_list)
		)

print('Parsing results and creating dictionary...', file=sys.stderr)
assets_dict = {}
for resolved_domain in resolved_domains:
	splited_resolved_domain = resolved_domain.split('-->')

	if(splited_resolved_domain[1].strip() in assets_dict.keys()):
		assets_dict[splited_resolved_domain[1].strip()].append(splited_resolved_domain[0].strip())
	else:
		assets_dict[splited_resolved_domain[1].strip()] = [splited_resolved_domain[0].strip()]

print('Detecting which asset is public and which private...', file=sys.stderr)
keys_to_remove = []
private_assets_dict = {}

for dict_key in assets_dict.keys():
	splited_dict_key = dict_key.split(',')
	is_public = False

	# Check if service is public
	for dict_key_frag in splited_dict_key:
		try:
			if (IP(dict_key_frag).iptype() == 'PUBLIC'):
				is_public = True
				break
		except:
			pass

	if(not is_public):
		private_assets_dict[dict_key] = assets_dict[dict_key]
		keys_to_remove.append(dict_key)
		
# Clean the public asset dictionary
for key_to_remove in keys_to_remove:
	assets_dict.pop(key_to_remove)

with open(public_assets_file, "w") as output_public_assets_file:
	output_public_assets_file.write(json.dumps(assets_dict, indent=4, sort_keys=True))

with open(private_assets_file, "w") as output_private_assets_file:
	output_private_assets_file.write(json.dumps(private_assets_dict, indent=4, sort_keys=True))
