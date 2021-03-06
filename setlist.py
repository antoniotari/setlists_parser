import operator
import urllib2
import json
import sys
import urllib
import datetime

def remove_previous_line() :
	sys.stdout.write("\033[F")

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1,length = 100, fill = '.'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    if (total == 0): 
        return

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    remove_previous_line()
    print("\r%s |%s| %s%% %s\r" % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total: 
        print()

OPTION_START_DATE = '-s'
OPTION_YEAR = '-y'
OPTION_END_DATE = '-e'
DATE_FORMAT = '%d-%m-%Y'

API_KEY = '1379c35f-1a6f-4d52-be50-24b865760a22'

artist_name = ''
start_date = datetime.datetime.strptime('1-1-1900', DATE_FORMAT)
end_date = datetime.datetime.now()
year = None

# parsing command line arguments
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]
    if (arg == OPTION_YEAR):
        i = i + 1
        year = sys.argv[i]
        print "year %s ,start and end date will be used to refine the search within this year"%year
        i = i + 1
    elif (arg == OPTION_START_DATE):
        i = i + 1
        start_date_str = sys.argv[i]
        start_date = datetime.datetime.strptime(start_date_str, DATE_FORMAT)
        print "starting date %s"%start_date
        i = i + 1
    elif (arg == OPTION_END_DATE):
        i = i + 1
        end_date_str = sys.argv[i]
        end_date = datetime.datetime.strptime(end_date_str, DATE_FORMAT)
        print "end date %s"%end_date
        i = i + 1
    else:
        artist_name = artist_name + ' ' + sys.argv[i]
	i = i + 1

artist_name = artist_name.strip()
artist_name_enc = urllib.quote_plus(artist_name)
url = "https://api.setlist.fm/rest/1.0/search/setlists?artistName=%s&p=%d"
# add the year to the url if passed as option
if (year != None):
	url = url + "&year=%s"%year

print "\n-- artist: %s --\n\n"%artist_name
page = 1

def make_request():
	request = urllib2.Request(url%(artist_name_enc, page))
	request.add_header('x-api-key' , API_KEY)
	request.add_header('Accept' , 'application/json')
	response_str = urllib2.urlopen(request).read()
	return json.loads(response_str)


# Loading the response data into a dict variable
# json.loads takes in only binary or string variables so using content to fetch binary content
# Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
jData = make_request() #json.loads(response_str)
setlists = jData
itemsPerPage = setlists['itemsPerPage']
total = setlists['total']
tot_pages = int(total) / int(itemsPerPage)
setlist = setlists['setlist']
page+=1
#remove this line after debug
#tot_pages = 11
# Initial call to print 0% progress
printProgressBar(page, tot_pages, prefix = "Progress:", suffix = "Complete", length = 50)
while (page<tot_pages):
    jData = make_request()
    setlists2 = jData
    setlist.extend(setlists2['setlist'])
    page+=1
    printProgressBar(page, tot_pages, prefix = "Progress:", suffix = "Complete", length = 50)
remove_previous_line()

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
                    song_list.append(song['name'])
            else:
                song_count+=1
                song_list.append(songs['name'])
    else:
        songs = sets['song']
        if (type(songs) is list):
            for song in songs:
                song_count+=1
                song_list.append(song['name'])
        else:
            song_count+=1
            song_list.append(songs['name'])


for item in setlist:
	eventDate = item['eventDate']
	eventDate_date = datetime.datetime.strptime(eventDate, DATE_FORMAT)
	if (eventDate_date >= start_date and eventDate_date <= end_date):
		sets1 = item['sets']
		if (type(sets1) is dict):
			sets = sets1['set']
			parse_set_list(sets)
		else:
			for setsElem in sets1:
				#sets = sets1['set']
				parse_set_list(setsElem)


lines = []
file_name = "%s__%s_%s_%s.txt"%(artist_name, start_date, end_date, year)
thefile = open(file_name, 'w')
for item in song_list:
    line_song = ("%s\n" % item).encode('utf-8') #.strip()
    thefile.write(line_song)
    lines.append(line_song)

#with open(file_name) as f:
#    lines = f.readlines()
#    print lines

dict = {}
for str in lines:
	key = str.rstrip('\n').lower()
	if ((key!='') and (key!=' ') and key!='play video' and key!='encore:'):
		if (key in dict):
			dict[key]=dict[key]+1
		else:
			dict[key]=1
sorted = sorted(dict.items(), key=operator.itemgetter(1))

rank_file_name = "%s_song_rank__%s_%s_%s.txt"%(artist_name, start_date, end_date, year)
thefile_rank = open(rank_file_name, 'w')
for tup in sorted:
    rank_line = "%s : %s"%(tup[0],tup[1])
    thefile_rank.write(rank_line+"\n")
    print rank_line

