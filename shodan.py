import shodan
import sys
import time
import json

ip_list_path = sys.argv[1]
output = sys.argv[2]

api_key = ""
api = shodan.Shodan(api_key)

ip_list = []

with open(ip_list_path,"r") as f:
	for ip in f.readlines():
		ip_list.append(ip.strip())

data = dict.fromkeys(ip_list)

for ip in ip_list:
	try:
		info = api.host(ip, history=True)
		data[ip] = info
	except shodan.exception.APIError:
		continue

with open(output, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
