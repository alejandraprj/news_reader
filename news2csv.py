#!/usr/local/bin/python3
import csv
import pandas as pd
from pygooglenews import GoogleNews

gn = GoogleNews() #lang = 'en', country = 'US'

Xmassearch = gn.search('intitle:Christmas', helper = True, from_ = '2019-12-01', to_= '2019-12-31')

print(Xmassearch['feed'].title)

for item in Xmassearch ['entries']:
  print(item['title'])

file = open("Christmassearch.csv", "w")
writer = csv.writer(file)

writer.writerow(["Xmassearch"])

file.close()
# - finish code
# - export first few, test
# - revise 
# - finish exporting everything