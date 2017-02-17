import operator
with open('megadeth_setlists.txt') as f:
	lines = f.readlines()
dict = {}
for str in lines:
	key = str.rstrip('\n').lower()
	if ((key!='') and (key!=' ') and key!='play video' and key!='encore:'):
		if (key in dict):
        		dict[key]=dict[key]+1
		else:
			dict[key]=1
sorted = sorted(dict.items(), key=operator.itemgetter(1))

for tup in sorted:
	print "%s : %s"%(tup[0],tup[1])

