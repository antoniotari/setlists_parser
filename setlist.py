import operator
import urllib2
import json

url = "http://api.setlist.fm/rest/0.1/search/setlists.json?artistName=%s&p=%d"
page = 1
response_str = urllib2.urlopen(url%('megadeth',page)).read()
# Loading the response data into a dict variable
# json.loads takes in only binary or string variables so using content to fetch binary content
# Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
jData = json.loads(response_str)
setlists = jData['setlists']
itemsPerPage = setlists['@itemsPerPage']
total = setlists['@total']
tot_pages = int(total) / int(itemsPerPage)
setlist = setlists['setlist']
page+=1
#remove this line after debug
#tot_pages = 11
while (page<tot_pages):
	response_str = urllib2.urlopen(url%('megadeth',page)).read()
	jData = json.loads(response_str)
	setlists2 = jData['setlists']
	setlist.extend(setlists2['setlist'])
	print(page)
	page+=1

with open('data.txt', 'w') as outfile:
	json.dump(setlist, outfile)

song_list = []

def parse_set_list(sets):
	song_count = 0
        if (type(sets) is list):
                        for set in sets:
                                songs = set['song']
                                if (type(songs) is list):
                                        for song in songs:
                                                song_count+=1
                                                song_list.append(song['@name'])
                                else:
                                        song_count+=1
                                        song_list.append(songs['@name'])
	else:
                        songs = sets['song']
                        if (type(songs) is list):
                                for song in songs:
                                        song_count+=1
                                        song_list.append(song['@name'])
                        else:
                                song_count+=1
                                song_list.append(songs['@name'])
	print(song_count)

for item in setlist:
	sets1 = item['sets']
	if (type(sets1) is dict):
		sets = sets1['set']
		parse_set_list(sets)
	else:
		for setsElem in sets1:	
			#sets = sets1['set']
                	parse_set_list(setsElem)		

#		if (type(sets) is list):
#			for set in sets:
#				songs = set['song']
#				if (type(songs) is list):
#					for song in songs:
#						song_count+=1
#						song_list.append(song['@name'])
#				else:
#					song_count+=1
#                                	song_list.append(songs['@name'])
#		else:
#			songs = sets['song']
#	               	if (type(songs) is list):
#				for song in songs:
#                			song_count+=1
#                			song_list.append(song['@name'])
#			else:
#				song_count+=1
#                                song_list.append(songs['@name'])

thefile = open('megadeth.txt', 'w')
for item in song_list:
	thefile.write("%s\n" % item)


with open('megadeth.txt') as f:
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

