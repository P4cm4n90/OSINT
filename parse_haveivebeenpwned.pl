# This script is for parsing breach data retrieved from haveivebeenpwned.com
# It extracts the most valuable attributes
# Made by Damian Pajszczyk (dspec)
import sys
import json
import hashlib
import re
import copy

email_data_path = sys.argv[1]
output = sys.argv[2]

parsed_attributes = ["Name","Domain", "BreachDate", "Description", "DataClasses"]

with open(email_data_path, "r") as f:
	email_data = json.loads(f.read())

email_list = list(email_data.keys())

parsed_emails = {}

for email in email_list:
	if email_data[email] == None:
		continue

	parsed_emails[email] = []

	for breach in json.loads(email_data[email]):
		breach_data =  {key: breach.get(key, None) for key in parsed_attributes}
		parsed_emails[email].append(breach_data)


with open(output, 'w', encoding='utf-8') as f:
    json.dump(parsed_emails, f, ensure_ascii=False, indent=4)
