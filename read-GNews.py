import feedparser
import pandas as pd
import re
import urllib
import argparse

# Feed URL
base_url = 'https://news.google.com/rss/search?q='

# Get the parameters

parser = argparse.ArgumentParser()

parser.add_argument('-q', action='append', dest='queries', nargs='+',
                    default=[],
                    help='Add all queries',
                    )

parser.add_argument('-l', action='store', dest='language',
                    default="en",
                    help='Store language')

parser.add_argument('-p', action='append', dest='locations', nargs='+',
                    default=[],
                    help='Add all places')


parser.add_argument('--version', action='version', version='%(prog)s 1.0')

# HTML cleanup function
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Prepare the data frame to store the items
d = []

# Access the feed and store data in d
def readFeed(url, query):

    feed = feedparser.parse(url)

    # Loop items in the feed
    for post in feed.entries:
        title = post.title
        link = post.link
        # Converting published date to aaaa/mm/dd
        pubDate = "%d/%02d/%02d" % (post.published_parsed.tm_year,\
            post.published_parsed.tm_mon, \
            post.published_parsed.tm_mday)

        description = cleanhtml(post.summary)
        source = post.source.title
        d.append((title, link, pubDate, description, source, query))
        #print(d)
    
    return d

# Get the parameters
args = parser.parse_args()

# Set the language (default = "en")
language = args.language.lower()

# Make sure there is at least one query
if len(args.queries) == 0:
    print("Please add at least one query using the -q parameter")
    exit

# Looping the different combination of queries and places

# Make sure there is at least one place
if len(args.locations) > 0:
    # Looping queries and places 
    for a in args.queries:
        for b in args.locations:
            query = ''.join(map(str, a))
            # URL encode the query and add quotes around it
            encoded_query = '"' + urllib.parse.quote_plus(query) + '"'
            place = urllib.parse.quote_plus(''.join(map(str, b)).upper() + ":" + ''.join(map(str, b)).lower()) 
            # Compose the URL
            url = base_url + encoded_query + "&hl=" + language + "&ceid=" + place 
            print("Reading now: ", url)
            # Read the Feed
            readFeed(url, query)
else: 
    # Just use the query(ies)
    for a in args.queries:   
        query = ''.join(map(str, a))
        # URL encode the query and add quotes around it
        encoded_query = '"' + urllib.parse.quote_plus(query) + '"'        
        # Compose the URL    
        url = base_url + encoded_query
        print("Reading now: ",url)
        # Read the Feed
        readFeed(url, query)

# Set the file name
cleanQuery = re.sub('\W+','', query)
file_name = cleanQuery + ".csv"

df = pd.DataFrame(d, columns=('Title', 'Link', 'pubDate', 'Description','Source', 'Query'))

# Remove all rows with the same link - you might want to comment this when using different keywords
df.drop_duplicates(subset ="Link", 
                     keep = False, inplace = True)
        
# Store data to CSV
df.to_csv(file_name, encoding='utf-8', index=False)
print(len(df), "Articles saved on ", file_name)