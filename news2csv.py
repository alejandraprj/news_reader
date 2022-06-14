# Python 3.9
# Program to obtain feeds w/ search results from Google News
  # and similar open access platforms
# Execute  : In the command line, write: 
           # python3 news2csv.py <source> <path>
# <source> : CSV source location for "Tag" and corresponding "Query"
# <path>   : directory where CSV results files will be located in
# Author   : Alejandra J. Perea Rojas

import pandas as pd
import feedparser
import re
import sys
import os
from urllib.parse import quote

base_url = "https://news.google.com/rss/search?q="
end_url = "&hl=en-US&gl=US&ceid=US%3Aen"

try:
  queries = pd.read_csv(sys.argv[1], sep=',')
  dir = sys.argv[2]
except FileNotFoundError:
  print("Source file not found.")
  sys.exit()

# Create directory to store CSV files
if not os.path.exists(dir):
  os.makedirs(dir)

# HTML cleanup function for description field
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Merge encoded query to make RSS Feed Link
def toRSS(tag, query):
  try:
    RSS_url = base_url + quote(query) + end_url
    return tag, RSS_url
    # print(url)
  except TypeError:
    print("Missing query from", tag + ". Stopping now.\n") 
    sys.exit()

# Reads feed and stores data in dataframe
def readFeed(tag, RSS_url):
  
  # Prepare the data frame to store the items
  data = []

  # Parse through items of RSS url
  feed = feedparser.parse(RSS_url)

  # Loop items in the feed
  for post in feed.entries:
    title = post.title
    link = post.link
    pubDate = "%d/%d/%d" % (post.published_parsed.tm_mon,\
              post.published_parsed.tm_mday,\
              post.published_parsed.tm_year)
    description = cleanhtml(post.summary)
    source = post.source.title
    data.append((title, link, pubDate, description, source, tag))

  return data

# Converts to CSV
def tocsv(tag, RSS_url):
  
  path = dir + "/" + tag + ".csv"
  print("Reading now: ", tag)
  print(RSS_url)

  # Feed dataframe
  df = pd.DataFrame(readFeed(tag, RSS_url),\
                    columns=('Title','Link','pubDate', 
                             'Description','Source','Tag'))

  # Remove all rows with the same link - 
    # might want to comment this when using different keywords
  df.drop_duplicates(subset ="Link", keep = False, inplace = True)
  
  # Store CSV file
  df.to_csv(path, encoding='utf-8', index=False)
  print(len(df), "Articles saved on", tag + ".csv\n")

print("\n")
# Iterate through each row and index
for row in queries.index:
  tag, RSS_url = toRSS(queries['Tag'][row], queries['Query'][row])
  tocsv(tag, RSS_url)
