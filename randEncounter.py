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
	rawr2.write(V)
	return(random.choice(V))
lineSort(rawr)
rawr.close()
rawr2.close()


