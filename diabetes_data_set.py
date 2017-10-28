import csv

def getDiabeticData():
	currentLine = []

	with open('diabetic_data.csv', 'r') as csvfile:
		for line in csvfile:
			temp = line.split(",")
			for x in temp:
				currentLine.append(x)
	
	count = 0
	iterator = 0
	i = 2
	j = 3
	k = 4
	z = 23
	imptAttributes = []

	for x in range(0, len(currentLine)):
		if x == i + imptAttCalc(count) or x == j + imptAttCalc(count) or x == k + imptAttCalc(count) or x == z + imptAttCalc(count):
			imptAttributes.append(currentLine[x])
			iterator += 0.25

			if iterator == 1.0:
				count += (int)(iterator)
				iterator = 0

	check = []
	temp = []
	for x in range(0,len(imptAttributes) - 1):
		temp.append(imptAttributes[x])
		if (x + 1) % 4 == 0:
			check.append(temp)
			temp = []

	print(check)

def imptAttCalc(count):
	return (50 * count)

def getData2():
	collection = []
	with open("file1-mto_nejm_puf_cells_20131025.dta", "rb") as f:
		byte = f.read(1)
		while byte != "":
			collection.append(byte)
        	# Do stuff with byte.
			byte = f.read(1)
			print(byte)
	print(collection)

getDiabeticData()
#getDiabeticData()