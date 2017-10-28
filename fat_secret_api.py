#docs: http://pyfatsecret.readthedocs.io/en/latest/api_docs.html

from fatsecret import Fatsecret
from key import KEY, SHARED_SECRET
import pprint

fs = Fatsecret(KEY, SHARED_SECRET)

foods = fs.foods_search("Tacos")

pp = pprint.PrettyPrinter(depth=6)
pp.pprint(foods)