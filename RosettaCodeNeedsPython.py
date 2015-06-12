__author__ = 'Mike'
from urllib.request import *
import re

base_url = "http://rosettacode.org"
category_url = base_url + "/wiki/Category:Draft_Programming_Tasks"

request = Request(category_url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
response = urlopen(request)

html = response.read().decode("utf-8") #decode bytes to a string

#Collect links to the articles
print("Collecting all drafts...")
p = re.compile('<li><a href="(/wiki/(?:\w|_)+)"')
articles = re.findall(p, html)

#Collect links that do not have python solutions
print("Eliminating drafts with Python solutions...")
no_python_sols = []
for extension in articles:
    art_url = base_url + extension
    request = Request(art_url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
    response = urlopen(request)

    art_html = response.read().decode("utf-8")
    if art_html.find('title="Edit section: Python">') == -1:
        no_python_sols.append(extension)

print()
print("There are", len(no_python_sols), "draft tasks without Python solutions.")
for art in no_python_sols:
    print("\t" + art.replace("_", " ")[6:] + "\t(" + base_url+art + ")")
