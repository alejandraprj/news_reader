import feedparser
import time
import pandas as pd
import re
import urllib.request as ur
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
 
 # HTML cleanup function
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Prepare the data frame to store the items
d = []

# Access the feed and store data in d
def readFeed(url, category):

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
        d.append((title, link, pubDate, description, source, category))
        # print(d)
    
    # Add delay between calls
    time.sleep(2)
    return d

# Converts to CSV
def tocsv(category, url):

    print("Reading now: ", category)
    readFeed(url, category)

    df = pd.DataFrame(d, columns=('Title', 'Link', 'pubDate', 'Description','Source', 'Category'))

    # Remove all rows with the same link - you might want to comment this when using different keywords
    df.drop_duplicates(subset ="Link", keep = False, inplace = True)
            
    # Store data to CSV
    filename = category + ".csv"
    df.to_csv(filename, encoding='utf-8', index=False)
    print(len(df), "Articles saved on ", filename)

urls = pd.read_csv('feeds.csv', sep=',')
for i, row in urls.iterrows():
    tocsv(row[0], row[1])
