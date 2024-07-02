# Script for parsing data extracted from shodan service
# It get's the most valuable data
# Made by Damian Pajszczyk (dpsec)
#
import sys
import json
import hashlib
import re
import copy

shodan_data_path = sys.argv[1]
output = sys.argv[2]

domain_regex = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'

parsed_data_attributes = ["domains", "hostnames", "services"]
services_data_attributes = ["port", "org", "data", "opts", "other"]

with open(shodan_data_path, "r") as f:
	shodan_data = json.loads(f.read())

ip_list = list(shodan_data.keys())

parsed_data = {ip: {attr: [] for attr in parsed_data_attributes} for ip in ip_list}

for ip in ip_list:
	if shodan_data[ip] is None:
		continue

	for data in shodan_data[ip]["data"]:
		for d in data.get("domains", []):
			if d not in parsed_data[ip]["domains"]:
				parsed_data[ip]["domains"].append(d)

		for h in data.get("hostnames", []):
			if h not in parsed_data[ip]["hostnames"]:
				parsed_data[ip]["hostnames"].append(h)

		if "port" in data:
			port = data["port"]
			existing_service = next((s for s in parsed_data[ip]["services"] if s["port"] == port), None)

			if existing_service:
				add_to_other = True
				if data["data"] == existing_service["data"]:
					add_to_other = False
				else:
					for other_data in existing_service["other"]:
						if len(data["data"]) == len(other_data) or data["data"] == other_data:
							add_to_other = False
							break
				
				if add_to_other:
					existing_service["other"].append(data["data"])
			else:
				service_data = {key: data.get(key, None) for key in services_data_attributes}
				service_data["other"] = []
				parsed_data[ip]["services"].append(service_data)

			potential_domains = re.findall(domain_regex, data["data"])
			for domain in potential_domains:
				if domain not in parsed_data[ip]["domains"]:
					parsed_data[ip]["domains"].append(domain)


filtered_data = {ip: data for ip, data in parsed_data.items() if data["services"] or data["domains"] or data["hostnames"]}

with open(output, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)
