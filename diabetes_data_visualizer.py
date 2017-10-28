import diabetes_data_set as data
import matplotlib.pyplot as plt

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
		
		race_graphs.append(current_race)
		current_race = {}
		race_x_y = {}

	return race_graphs

def main():
	print(draw())

main()

