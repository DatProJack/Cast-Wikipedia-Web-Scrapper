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


def parse_file(url, destination):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    titleparse = doc.find('title')
    s = str(titleparse.text)
    result = re.split(r"[-(]\s*", s)
    title = result[0].strip()
    infobox = doc.find_all("th", {"class": "infobox-label"})
    parsed_infobox = []
    for element in infobox:
        data = element.find_next()
        content = str(data.text).strip()
        content = content.replace("\n", "\",\" ")
        parsed_infobox.append(str(element.text) + ": " + content)

    headers = doc.find_all("h2")
    #charactertypes = doc.find_all("h3")

    bulletlist = None
    for tag in headers:
        if(tag.get_text().find('Cast')>=0):
            bulletlist = tag
            break
        
    file = open('./parsed_csv_files/' + destination + '.csv', 'a', newline='', encoding='utf-8')
    writer = csv.writer(file)


    if(bulletlist is None):
        writer.writerow([title, '404 ERROR'])
        return
    bulletlist = bulletlist.find_next()

    firstrow = [title,"1"]
    firstrow.extend(parsed_infobox)
    writer.writerow(firstrow)


    iteration = 2
    while bulletlist.name!="h2":
        if bulletlist.name=="ul" or bulletlist.name=="td":#works better for bullet points, not so great for tables
            #if(i < len(charactertypes) - 1 and bulletlist.sourceline > charactertypes[i+1].sourceline):#for tables it should be easier...
            #    i = i + 1
            s = "Cast"
            #if(len(charactertypes) != 0):
            #    s = str(charactertypes[i].text)
            #chartype = re.split(r"[-(,\[*]\s*", s)
            #chartype = chartype[0].strip()
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
                    writer.writerow([title,iteration,actorname,charname,description])#write here
                    iteration = iteration + 1
        bulletlist = bulletlist.find_next()




file = open('urls.csv', 'r')
i = 1

for line in file.readlines():
    print(i)
    i = i + 1
    parse_file(line.strip(), 'product')