import csv
import math

from random import randint

current_line = []

with open('diabetic_data.csv', 'r') as csvfile:
	for line in csvfile:
		temp = line.split(",")
		for x in temp:
			current_line.append(x)

count = 0
iterator = 0
i = 2
j = 3
k = 4
z = 23
impt_attributes = []

for x in range(0, len(current_line)):
	if x == i + (50 * count) or x == j + (50 * count) or x == k + (50 * count) or x == z + (50 * count):
		impt_attributes.append(current_line[x])
		iterator += 0.25

		if iterator == 1.0:
			count += (int)(iterator)
			iterator = 0

sorted_Att = []
temp = []
for x in range(0,len(impt_attributes) - 1):
	temp.append(impt_attributes[x])
	if (x + 1) % 4 == 0:
		sorted_Att.append(temp)
		temp = []

diabetic_data = sorted_Att

def get_mean():
	collection = []
	for x in diabetic_data:
		if "None" not in x and "Norm" not in x:
			collection.append(x[2])
	
	numbers = []
	for x in collection:
		numbers.append((int)(x[1]))

	computed_sum = sum(numbers)
	mean = sum(numbers) / len(numbers)

	return math.ceil(mean)

def change_to_mean():
	mean = get_mean()
	global diabetic_data

	for x in diabetic_data:
		if "None" in x or "Norm" in x:
			x[3] = ">" + (str)(mean)

def impt_att_calc(count):
	return (50 * count)

def get_none():
	count = 0
	for x in diabetic_data:
		if "None" in x:
			count+=1

	print(count)

def get_race():
	race = []

	for x in diabetic_data:
		if x[0] not in race and x[0] != "?":
			race.append(x[0])
	
	return race

def get_sex():
	sex = []

	for x in diabetic_data:
		if x[1] not in sex:
			sex.append(x[1])

	return sex

def get_age(race, sex):
	age = []

	for x in diabetic_data:
		if x[0] == race and x[1] == sex:
			age_range = x[2].split("-")
			lower_age = (int)(age_range[0][1:])
			upper_age = (int)(age_range[1][:-1])
			age.append(randint(lower_age, upper_age))

	return age

def get_a1c(race, sex):
	a1c = []

	for x in diabetic_data:
		if x[0] == race and x[1] == sex:
			current_a1c = (int)(x[3][1:])
			a1c.append(current_a1c)

	return a1c

def main():
	collection = diabetic_data
	mean = get_mean()
	print(get_race())
change_to_mean()
main()