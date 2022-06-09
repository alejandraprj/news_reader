import feedparser
import time
import sys
import pandas as pd
import re
import urllib
import urllib.request as ur
import argparse
import bs4

base_url = "https://news.google.com/rss/search?q=(%22Sensing%22%20OR%20%22Sensors%22)%20AND%20when%3A1y%20AND%20(%22Wildlife%22%20OR%20((%22Protected%20Areas%22%20OR%20%22Conservation%22)%20AND%20(%22Animals%22%20OR%20%22Biodiversity%22)))&hl=en-US&gl=US&ceid=US%3Aen"

parser = argparse.ArgumentParser()

# Get Alexa Rank - remember it only works from USA so you need a proxy
def getMetrics(url):
    cleanDomain = '/'.join(url.split('/')[:3])
    try:
        alexa_rank = bs4.BeautifulSoup(ur.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml").find("REACH")["RANK"]
    except:
        alexa_rank = None
    return alexa_rank
 
 # HTML cleanup function
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Prepare the data frame to store the items
d = []

# Access the feed and store data in d
def readFeed(url):

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
        # Get Alexa Rank
        alexa_rank = getMetrics(link)
        d.append((title, link, pubDate, description, source, alexa_rank))
        print(d)
    
    # Add delay between calls
    time.sleep(2)
    return d

# Read the Feed
print("Reading now: ", base_url)
readFeed(base_url)

file_name = "simple.csv"

df = pd.DataFrame(d, columns=('Title', 'Link', 'pubDate', 'Description','Source', 'Alexa Rank'))

# Remove all rows with the same link - you might want to comment this when using different keywords
df.drop_duplicates(subset ="Link", 
                     keep = False, inplace = True)
        
# Store data to CSV
df.to_csv(file_name, encoding='utf-8', index=False)
print(len(df), "Articles saved on ", file_name)