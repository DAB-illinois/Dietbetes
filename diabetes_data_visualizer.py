import diabetes_data_set as data

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
DATABASE_NAME = "databetes_app"
TABLE_NAME = "diabetes_data_set"
db = client[DATABASE_NAME]

def draw():
	race = data.get_race()
	sex = data.get_sex()

	race_graphs = []
	current_race = {}
	race_x_y = {}

	for x in race:
		for i in sex:
			age = data.get_age(x, i)
			a1c = data.get_a1c(x, i)

			race_x_y["age"] = age
			race_x_y["a1c"] = a1c
			current_race["" + x + "," + i] = race_x_y
		
			db_data = {"race/gender":"" + x.lower() + "," + i.lower(), "graph":race_x_y}
			db[TABLE_NAME].insert_one(db_data)
			race_graphs.append(current_race)
			current_race = {}
			race_x_y = {}

	return race_graphs

def main():
	print(draw())

main()

