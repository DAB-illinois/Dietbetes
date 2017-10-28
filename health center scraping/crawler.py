from urllib.request import Request, urlopen
import lxml.html
import re

base_url = "https://npidb.org/organizations/ambulatory_health_care/federally-qualified-health-center-fqhc_261qf0400x/?page="
inner_base_url = "https://npidb.org"

MAX = 202

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
DATABASE_NAME = "databetes_app"
TABLE_NAME = "health_centers"
db = client[DATABASE_NAME]

def add(dic):
	posts = db[TABLE_NAME]
	result = posts.insert_one(dic)
	print('One post: {0}'.format(result.inserted_id))

def get_page(url):
	req = Request(inner_url, headers={'User-Agent': 'Mozilla/5.0'})
	urlRequest = urlopen(inner_url)
	urlLxml = lxml.html.parse(urlRequest)
	name = ""
	has_name = False
	address = ""
	tele = ""
	for element in urlLxml.iter():
		attrib = element.attrib

		if element.tag == "img" and not has_name:
			if "alt" in attrib:
				if name == "NPI Lookup":
					has_name = True
				name = attrib["alt"]
		if element.tag == "address":
			address = element.text_content()
			final = ""
			address = re.split('\t|\r|\n|\u2002',address)
			for e in address:
				if e != "":
					final += e +" "
			address = final.strip()
		if element.tag == "span" and "itemprop" in attrib and attrib['itemprop'] == "telephone":
			tele = element.text_content()
	return name, address, tele, address.split(" ")[-2]

data = {}

for i in range(1, MAX + 1):
	url = base_url + str(i)
	print(i)

	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	urlRequest = urlopen(req)
	urlLxml = lxml.html.parse(urlRequest)

	for element in urlLxml.iter():
		if element.tag == "a":
			attrib = element.attrib
			if "/organizations/ambulatory_health_care/federally-qualified-health-center-fqhc_261qf0400x/" in attrib["href"] and ".aspx" in attrib["href"]:
				inner_url = inner_base_url + attrib["href"]
				
				name, address, tele, state = get_page(inner_url)
				if state in data:
					data[state].append({"name": name, "address": address, "telephone": tele})
				else:
					data[state] = [{"name": name, "address": address, "telephone": tele}]
				break
	break

for i, j in data.items():
	add({i:j})