'''Uses the placekitten API to download pictures of cats with dimensions input by the user.'''
from urllib.request import *
from json import load

url = "http://placekitten.com/g"
url += "/" + input("Width? ")
url += "/" + input("Height? ")
print(url)

try:
    request = Request(url)
    response = urlopen(request)
    kitteh = response.read()
    print()
    if kitteh != bytes(0):
        with open("cat.png", "wb") as picture:
           picture.write(kitteh)
           print("Output as cat.png")
    else:
        print("There was no image of that size.")
except URLError:
    print("no kittehz")
