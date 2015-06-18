'''Scrapes every pixel art image from this website'''
__author__ = 'Mike'
from urllib.request import *
import os
import re


BASE_URL = "http://pousse.rapiere.free.fr/tome/"
PICTURE_PATTERN = re.compile(r'<img src="((?:\w|-|/|%)+\.(?:gif|PNG))"')
LINK_PATTERN = re.compile(r'(tiles/\w+/(?:\w|-)+\.htm)')
DIRECTORY_PATTERN = re.compile(r'((?:\w|/)+/)')


def readPageData(url_extension):
    '''Return page data as bytes'''
    url = BASE_URL + url_extension
    request = Request(url, headers={"User-Agent" : "Magic Browser"}) #Spoofing as a browser
    response = urlopen(request)
    return response.read()


def assureDirectoryExistence(dir_name):
    '''Creates a directory if it does not exist. Learned how to do this with this project.'''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def saveImage(pic_extension):
    '''Save the image to a file'''
    path_name = pic_extension.replace("%20", "_")
    assureDirectoryExistence(DIRECTORY_PATTERN.findall(path_name)[0])

    if not os.path.exists(path_name):
        print("downloading", path_name)
        pic_data = readPageData(pic_extension)

        with open(path_name, "wb") as p:
            if pic_data != bytes(0):
                p.write(pic_data)


def main():
    hub = readPageData("tome-tiles.htm").decode("utf-8")
    links = LINK_PATTERN.findall(hub)

    for extension in links:
        picture_links = PICTURE_PATTERN.findall(readPageData(extension).decode("utf-8"))
        print("opening", BASE_URL + extension)
        remove = re.search(r"/(?:\w|-)+\.htm", extension)
        extension = extension[:remove.start()] + "/" + extension[remove.end():]
        for pic in picture_links:
            saveImage(extension + pic)


main()
