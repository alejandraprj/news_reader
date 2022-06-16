# Python 3.9
# Program to obtain feeds w/ search results from Google News
  # and similar open access platforms
# Execute  : In the command line, write: 
           # python3 news2csv.py <source> <path>
           # <source> : CSV source for "Tag" and corresponding "Query"
           # <path>   : directory where CSV results files will go
# Example  : python3 news2csv.py source.csv path
# Author   : Alejandra J. Perea Rojas

import pandas as pd
import feedparser
import re
import sys
import os
from urllib.parse import quote

# Printing to Log File
log = open('logfile.txt', 'w+')

base_url = "https://news.google.com/rss/search?q="
og_url = "https://news.google.com/search?q="
end_url = "&hl=en-US&gl=US&ceid=US%3Aen"

# Read source file and name result directory
try:
  rows = pd.read_csv(sys.argv[1], sep=',')
  dir = sys.argv[2]
  # Create directory to store CSV files
  if not os.path.exists(dir):
    os.makedirs(dir)
except FileNotFoundError:
  print("Source file not found.")
  sys.exit()

# Encodes query and returns links to be read
def toRSS(tag, query):
  try:
    encoded = quote(query) + end_url
    RSS_url = base_url + encoded
    og = og_url + encoded
    return tag, RSS_url, og
  except TypeError:
    print("Missing query from", tag + ". Stopping now.\n") 
    sys.exit()

# Cleans HTML for description field
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Reads feed and returns dataframe
def readFeed(tag, RSS_url):
  
  # Prepare the data frame to store the items
  data = []

  # Parse through items of RSS url
  feed = feedparser.parse(RSS_url)

  # Loop items in the feed
  for post in feed.entries:

    title = post.title
    link = post.link
    pubDate = "%d/%d/%d" % \
             (post.published_parsed.tm_mon, \
              post.published_parsed.tm_mday,\
              post.published_parsed.tm_year)
    description = cleanhtml(post.summary)
    source = post.source.title

    data.append((title, link, pubDate,\
                 description, source, tag))

  return data

# Converts to CSV and stores it
def tocsv(tag, RSS_url, og):
  
  path = dir + "/" + tag + ".csv"

  # Prints and saves processing log 
  print("Reading now: ", tag, "\n", og)
  print("Reading now: ", tag, "\n", og, file=log)

  # Feed dataframe
  df = pd.DataFrame(readFeed(tag, RSS_url),\
                    columns=('Title','Link','pubDate', 
                             'Description','Source','Tag'))

  # Remove all rows with the same link - 
    # might want to comment this when using different keywords
  df.drop_duplicates(subset ="Link", keep = False, inplace = True)
  
  # Store CSV file
  df.to_csv(path, encoding='utf-8', index=False)

  # Print and save number of articles for a tag
  print(len(df), "Articles saved on", tag + ".csv\n")
  print(len(df), "Articles saved on", tag + ".csv\n", file=log)

# Iterate through each row and index
for row in rows.index:
  tag, RSS_link, og = toRSS(rows['Tag'][row], rows['Query'][row])
  tocsv(tag, RSS_link, og)
