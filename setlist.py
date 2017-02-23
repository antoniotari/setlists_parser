import operator
import urllib2
import json
import sys
import urllib

OPTION_START_DATE = '-s'
OPTION_END_DATE = '-e'

artist_name = ''
start_date = ''
end_date = ''

# parsing command line arguments
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if (arg == OPTION_START_DATE):
        i = i + 1
        start_date = sys.argv[i]
        print "starting date %s"%start_date
    elif (arg == OPTION_END_DATE):
        i = i + 1
        end_date = sys.argv[i]
        print "end date %s"%end_date
    else:
        artist_name = artist_name + ' ' + arg
	i = i + 1

artist_name = artist_name.strip()
artist_name_enc = urllib.quote_plus(artist_name)
url = "http://api.setlist.fm/rest/0.1/search/setlists.json?artistName=%s&p=%d"
print artist_name
page = 1
response_str = urllib2.urlopen(url%(artist_name_enc,page)).read()
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
    response_str = urllib2.urlopen(url%(artist_name_enc,page)).read()
    #print url%(artist_name_enc,page)
    jData = json.loads(response_str)
    setlists2 = jData['setlists']
    setlist.extend(setlists2['setlist'])
    print(page)
    page+=1

with open("data_%s.txt"%artist_name, 'w') as outfile:
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


file_name = "%s.txt"%artist_name
thefile = open(file_name, 'w')
for item in song_list:
    line_song = ("%s\n" % item).encode('utf-8') #.strip()
    thefile.write(line_song)


with open(file_name) as f:
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

rank_file_name = "%s_song_rank.txt"%artist_name
thefile_rank = open(rank_file_name, 'w')
for tup in sorted:
    rank_line = "%s : %s"%(tup[0],tup[1])
    thefile_rank.write(rank_line+"\n")
    print rank_line

