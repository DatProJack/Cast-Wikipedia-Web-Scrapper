from bs4 import BeautifulSoup
import requests
import re
import csv



def clean(s):#cleans the string to remove characters between []
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in s:
        if i == '[':
            skip1c += 1
        #elif i == '(':
            #skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        #elif i == ')'and skip2c > 0:
            #skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

url = "https://en.wikipedia.org/wiki/The_Marvelous_Mrs._Maisel"#insert any url here-- only works for wikipedia tv series urls

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")


headers = doc.find_all("h2")

for tag in headers:
    if(tag.get_text().find('Cast')>=0):
        bulletlist = tag
        break

scraped_sentences = []
bulletlist = bulletlist.find_next(['ul', 'td'])

while bulletlist.name!="h2":
    if bulletlist.name=="ul" or bulletlist.name=="td":#works better for bullet points, not so great for tables
        for tag in bulletlist:
            s = str(tag.text)
            s = clean(s).strip() #cleaning up and removing whitespace
            if(len(s)!=0):#skips over if the string is empty
                scraped_sentences.append(s)
    bulletlist = bulletlist.find_next()


with open('parsedtext.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  for s in scraped_sentences:
    writer.writerow([s])