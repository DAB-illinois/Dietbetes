data = {}
with open("gi_indices.txt", 'r') as f:
	a = f.readlines()
	for line in a:
		l = line.split(".")

		if len(l) > 2:
			print(line)
			


