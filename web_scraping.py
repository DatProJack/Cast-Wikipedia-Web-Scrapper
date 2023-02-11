from bs4 import BeautifulSoup
import requests
import re
import csv



def clean(s):#cleans the string to remove characters between [] ()
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in s:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret

url = "https://en.wikipedia.org/wiki/Joy_of_Life_(TV_series)"#insert any url here-- only works for wikipedia tv series urls

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

titleparse = doc.find('title')
s = str(titleparse.text)
result = re.split(r"[-(]\s*", s)
title = result[0].strip()


headers = doc.find_all("h2")
charactertypes = doc.find_all("h3")

for tag in headers:
    if(tag.get_text().find('Cast')>=0):
        bulletlist = tag
        break

scraped_sentences = []
bulletlist = bulletlist.find_next()

file = open('parsedtext.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)

i=0
iteration = 1
while bulletlist.name!="h2":
    if bulletlist.name=="ul" or bulletlist.name=="td":#works better for bullet points, not so great for tables
        if(bulletlist.sourceline > charactertypes[i+1].sourceline):#for tables it should be easier...
            i = i + 1
        s = str(charactertypes[i].text)
        chartype = re.split(r"[-(,\[*]\s*", s)
        chartype = chartype[0].strip()
        for tag in bulletlist:
            s = str(tag.text)
            s = clean(s).strip() #cleaning up and removing whitespace
            #from s: split at the first as and first comma
            if(len(s)!=0):#skips over if the string is empty
                s = s.split(" as ", maxsplit = 1)
                actorname = clean(s[0])
                if(len(s)==1):
                    continue
                s = s[1].split(",", maxsplit = 1)
                charname = clean(s[0])
                description = ""
                if(len(s)>1):
                    description = clean(s[1])
                writer.writerow([title,chartype,iteration,actorname,charname,description])#write here
                iteration = iteration + 1

            
    bulletlist = bulletlist.find_next()