import requests
# Unfinished script created to extract data from security trails service
#
#  Made by Damian Pajszczyk (dpsec)
#
import sys

ip_list_filepath = sys.argv[1]
output = ""

api_key = ""
url = "https://api.securitytrails.com/v1/search/list"

### We want here to get data related to ip addresses and domains

def get_iplist():
	ip_list = []
	with open(ip_list_filepath, "r") as f:
		for ip in f.readlines():
			ip_list.append(ip.strip())

	return ip_list


def get_data(query):
	json_data = { "query":query }
	headers = { "APIKEY":api_key }
	r = requests.post(url,json=json_data,headers=headers)
	return r


ip_list = get_iplist()

temp_query = ""

for ip in ip_list:
	temp_query += f"ip in {ip} OR "

query = temp_query[:-4]

response = get_data(query)
print(response.text)
print(response.json)
