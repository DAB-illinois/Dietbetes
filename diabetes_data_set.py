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

	print(imptAttributes)

def imptAttCalc(count):
	return (50 * count)

getDiabeticData()