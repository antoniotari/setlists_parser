# setlists_parser
parse a document with setlists from setlists.fm and returns the most played songs

#usage
`./setlists -y <year> -s <starting_date> -e <end_date> <artist_name>` <br>
options <b>-y</b>, <b>-s</b> and <b>-e</b> are optional <br>
the date format for <i>-s</i> and <i>-e</i> options must be <b>dd-mm-yyyy</b>, for example <b><i>24-11-2001</i></b> <br>
the date format for <i>-y</i> is <b>yyyy</b> , if using the year option the search will be resctricted to that year no matter what start and end dates are<br>
omitting the end date will assume current date <br>
spaces are allowed in the artist name<br><br>
ie.<br>
`./setlist megadeth`<br>
`./setlist children of bodom` <br>
`./setlist.py -s 1-1-1998 -e 1-10-2011 children of bodom`


