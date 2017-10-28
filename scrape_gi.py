from urllib.request import Request, urlopen

base_url = "http://www.glycemicindex.com/foodSearch.php?ak=detail&num="

MAX_INDEX = 2688
NAME_STRING = b'\t\t\t\t\t\t\t\t\t\t\t\t\t<td width="25%"><strong>Food Name</strong></td>\n'
GI_STRING = b'\t\t\t\t\t\t\t\t\t\t\t\t\t<td><strong>GI (vs Glucose)</strong></td>\n'

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
DATABASE_NAME = "databetes_app"

db = client[TEST_DATABASE_NAME]

def add_to_db(dic):
	table = db.gi_indexes
	result = table.insert_one(dic)
	print('One post: {0}'.format(result.inserted_id))

def get_start_end_index(html, string_to_find):
	string_index = html.index(string_to_find)
	string_html = html[string_index + 1].decode()
	start = string_html.index(">")
	end = string_html[start:].index("<") + start
	return start, end, string_html

gi_data = {}

for i in range(1, MAX_INDEX):
	print(i)
	url = base_url + str(i)

	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	urlRequest = urlopen(req)
	html = urlRequest.readlines()

	start, end, item_html = get_start_end_index(html, NAME_STRING)
	name = item_html[start + 1:end].split(",")[0]
	start, end, item_html = get_start_end_index(html, GI_STRING)
	gi_index = item_html[start + 1:end]

	if name in gi_data:
		gi_data[name].append(gi_index)
	else:
		gi_data[name] = [gi_index]

for i, j in gi_data:
	l = len(j)
	s = sum(j)
	avg = int((s/l)*100)/100;
	add_to_db({i, str(avg)})