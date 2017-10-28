from urllib.request import Request, urlopen

LOOK_FOR = b'\t\t\t\t\t\t\t\t\t\t<div class="factTitle">Carbs</div>\r\n'

def get_carb_per_serving(url):
	urlRequest = urlopen(Request(url))
	html = urlRequest.readlines()
	html_str = str(html)
	ind = html.index(LOOK_FOR)+1
	start = html[ind].decode().index(">")+1
	carbs = html[ind].decode()[start:]
	carbs = carbs[:carbs.index("g<")]
	print(carbs)