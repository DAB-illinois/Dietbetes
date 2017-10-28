import urllib

LOOK_FOR = '\t\t\t\t\t\t\t\t\t\t<div class="factTitle">Carbs</div>\r\n'

def get_carb_per_serving(url):
	html = urllib.urlopen(url)
	html = html.readlines()
	html_str = str(html)
	item = html[html.index(LOOK_FOR)+1]
	item = item[item.index(">")+1:]
	result = item[:item.index("g<")]
	
	return float(result)
