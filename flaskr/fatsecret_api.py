#docs: http://pyfatsecret.readthedocs.io/en/latest/api_docs.html

from fatsecret import Fatsecret
from key import KEY, SHARED_SECRET

fs = Fatsecret(KEY, SHARED_SECRET)

foods = fs.foods_search("Tacos")

def search_food(query):
	foods = fs.foods_search(query)
	return foods