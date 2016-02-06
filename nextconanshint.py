'''Scrapes the detectiveconanworld list of Detective Conan anime episodes. (get_data)
returns a wikitable of the episode number, episode title, and next conan's hint. (convert_data)

Used to construct the framework for http://www.detectiveconanworld.com/wiki/Next_Conan%27s_Hint'''

import requests
import re
from bs4 import BeautifulSoup

def zext3(string):
    while len(string) < 3:
        string = "0" + string
    return string
    
def get_data():
    pageurl = 'http://www.detectiveconanworld.com/wiki/Anime'

    html = requests.get(pageurl).text
    soup = BeautifulSoup(html, 'html.parser')

    #Constants for navigating cols
    EP_NUM = 1 #Japan
    EP_NAME = 3
    HINT = 9

    ep_data = []

    for row in soup.find_all('tr')[2:]: #Start at 2 to cut off what aren't rows
        cols = row.get_text().split("\n")

        # Not a data row
        if not cols[EP_NUM].strip().isdigit():
            continue

        if int(cols[EP_NUM]) > len(ep_data): # Not a rerun
            ep = dict()
            ep["num"] = cols[EP_NUM].strip()
            if "(" not in cols[EP_NAME]:
                ep["name"] = cols[EP_NAME].strip()
            else:
                ep["name"] = re.sub(r"\([^)]*?\)", "", cols[EP_NAME]).strip()
                ep["name"] += "|{}".format(cols[EP_NAME].strip())
            ep["hint"] = cols[HINT].strip()
            ep_data.append(ep)
        else: # A rerun
            ep = ep_data[int(cols[EP_NUM])-1] 
            if ep["hint"] != cols[HINT]:
                ep["hint"] += " / {}".format(cols[HINT])
            
    return ep_data

def convert_data(data):
    output = '''{| class="wikitable" 
|-
! #
! Episode Name
! Next Conan Hint
! Image
! Rerun/Remaster Image
|-'''

    for ep in data:
        output = output + '''
| {}
| [[{}]]
| {}
|
|
|-'''.format(zext3(ep["num"]), ep["name"], ep["hint"])

    output += "\n|}"
    return output

def main():
  data = get_data()
  print(convert_data(data))

if __name__ = "__main__":
  main()
