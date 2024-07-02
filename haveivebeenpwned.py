import sys
import json
import time
import re
import requests

api_key = ""

emails_path = sys.argv[1]
emails_count = 0

def get_emails(emails_path):
	emails = []
	with open(emails_path, "r") as f:
		for e in f.readlines():
			emails.append(e.strip())

	return emails


def get_data(email):
	global req_number

	headers = {"hibp-api-key": api_key,
				"User-Agent": "Super tester"}

	r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false", headers=headers)

	if r.status_code == 404:
		return None

	if r.status_code == 429:
		time.sleep(10)
		get_data(email)

	if r.status_code == 200:
		return r.text


def get_all_data_parse(emails):
	emails_count = len(emails)

	data = dict.fromkeys(emails,[])

	for i in range(0,len(emails)):

		print(f"{str((i/len(emails)) * 100)} %",end="\r")

		k = emails[i]
		breached_data = get_data(k)
		data[k] = breached_data
		time.sleep(11)

	return data

emails = get_emails(emails_path)
data = get_all_data_parse(emails)

with open('./data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
