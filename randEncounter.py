import random
rawr = open('rawr.txt','r')
rawr2 = open('actualGuess.txt','w')

def lineSort(rawr):
	lines = []
	oList = []
	with open('rawr.txt','r') as f:
		lines = f.readlines()
	random_line_num = random.randrange(0, len(lines))
	oList.append(lines[random_line_num])
	V = oList[0]
	splitOList = V.split()
	randomEncounter = random.choice(splitOList)
	rawr2.write(randomEncounter)
	return(random.choice(splitOList))
lineSort(rawr)
rawr.close()
rawr2.close()


