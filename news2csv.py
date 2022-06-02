import pandas as pd
import csv
from pygooglenews import GoogleNews

gn = GoogleNews (lang = 'en', country = 'UK') 

Xmassearch = gn.search('intitle:Christmas', helper = True, from_ = '2019-12-01', to_= '2019-12-31')

print(Xmassearch['feed'].title)

for item in Xmassearch ['entries']:
  print(item['title'])

file = open("Christmassearch.csv", "w")
writer = csv.writer(file)

writer.writerow(["Xmassearch"])

file.close()