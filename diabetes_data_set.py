import csv

def get_diabetic_data():
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
	imptAttributes = []

	for x in range(0, len(currentLine)):
		if x == i + impt_att_calc(count) or x == j + impt_att_calc(count) or x == k + impt_att_calc(count) or x == z + impt_att_calc(count):
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

	return(sorted_Att)

def get_mean(sorted_Att):
	collection = []
	for x in sorted_Att):
		if "None" not in x and "Norm" not in x:
			collection.append(x[2])
	
	numbers = []
	for x in collection:
		numbers.append(x[1])

	computed_sum = sum(numbers)
	mean = sum(numbers) / len(numbers)

	return (int)(mean)

def change_to_mean(mean):
	

def impt_att_calc(count):
	return (50 * count)

def get_none():
	collection = get_diabetic_data()

	count = 0
	for x in collection:
		if "None" in x:
			count+=1

	print(count)


# def getData2():
# 	collection = []
# 	with open("file1-mto_nejm_puf_cells_20131025.dta", "rb") as f:
# 		byte = f.read(1)
# 		while byte != "":
# 			collection.append(byte)
#         	# Do stuff with byte.
# 			byte = f.read(1)
# 			print(byte)
# 	print(collection)