from urllib.request import Request, urlopen
import urllib.error
import threading

base_url = "http://www.glycemicindex.com/foodSearch.php?ak=detail&num="

MAX_INDEX = 2688
NAME_STRING = 211
GI_STRING = 220

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
DATABASE_NAME = "databetes_app"

db = client[DATABASE_NAME]

def add_to_db(dic):
	table = db.gi_indexes
	result = table.insert_one(dic)
	print('One post: {0}'.format(result.inserted_id))

def get_start_end_index(html, index_to_get):
	string_html = html[index_to_get].decode()
	start = string_html.index(">")
	end = string_html[start:].index("<") + start

	return string_html[start + 1:end]

gi_data = {}

for i in range(1, MAX_INDEX):
	print(i)
	url = base_url + str(i)

	try:
		urlRequest = urlopen(Request(url))
		html = urlRequest.readlines()
	except urllib.error.HTTPError:
		continue

	name = get_start_end_index(html, NAME_STRING).split(",")[0]
	gi_index = float(get_start_end_index(html, GI_STRING))

	if name in gi_data:
		gi_data[name].append(gi_index)
	else:
		gi_data[name] = [gi_index]

with open("gi_indices.txt", "w") as f:
	for i, j in gi_data.items():
		l = len(j)
		s = sum(j)
		avg = int((s/l)*100)/100;
		f.write(i+":"+str(avg)+"\n")