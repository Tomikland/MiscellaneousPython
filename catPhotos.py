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
    print(kitteh)
    with open("cat.png", "wb") as picture:
        picture.write(kitteh)
        picture.close()
except URLError:
    print("no kittehz")
