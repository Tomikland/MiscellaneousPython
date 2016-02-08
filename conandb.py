'''A scraper to create a detective conan information db'''

__author__ = 'Mike'
import re
import requests

URL_START = 'http://www.detectiveconanworld.com/wiki/'
CATEGORY_URL_END = 'Category:Appearances'
PAGE_URL_END = '_Appearances'

def get_characters():
    html = requests.get(URL_START + CATEGORY_URL_END).text
    start = html.find('<table')
    end = html.find('</table', start)
    return re.findall(r'<li>.+>(.+) Appearances</a>', html[start:end])

def console_print_char_and_apps(characters, appearance_lists):
    for personID in range(len(appearance_lists)):
        print(characters[personID] + ":", len(appearance_lists[personID]))
        print(appearance_lists[personID])
    print("characters", len(characters))
    print("appearance lists", len(appearance_lists))

def reverse_appearances(the_name, the_characters, the_appearance_lists):
    """Some characters, such as Conan, have lists of episodes in which they DON'T appear."""
    conan = the_characters.index(the_name)
    episodes_with_conan = list(range(1, 800))
    #print(episodes_with_conan)
    #print(conan)
    #print(the_appearance_lists[conan])
    for ep in the_appearance_lists[conan]:
        print("Removed", ep)
        del episodes_with_conan[int(ep)-1]
    the_appearance_lists[conan] = episodes_with_conan

def getEpisodeTitles():
    pass
def main():
    print("Getting characters")
    characters = get_characters()
    appearance_lists = []
    print("Extracting appearances")
    i = 1
    for person in characters[0:]:
        html = requests.get(URL_START + person + PAGE_URL_END).text
        start = html.find(r'=edit&amp;section=2')
        end = html.find('/table', start)
        episodes = re.findall(r"<li>.+<b>Episode (.+?)</b>", html[start:end])
        appearance_lists.append(episodes)
        print(i)
        i+=1

    #Remove nonanime characters
    print("Removing nonanime characters")
    nonanime_personIDs = []
    for personID in range(len(appearance_lists)):
        if len(appearance_lists[personID]) == 0:
            nonanime_personIDs.append(personID)

    deleted_count = 0
    for id in nonanime_personIDs:
        del appearance_lists[id - deleted_count]
        del characters[id - deleted_count]
        deleted_count += 1

    print("\n\n\n\n", appearance_lists,"\n\n\n\n")

    print("Reversing Characters")
    chars_needing_reverse = ["Conan Edogawa", "Ran Mouri", "Kogoro Mouri"]
    for name in chars_needing_reverse:
        print(name)
        print(appearance_lists[characters.index(name)])
        reverse_appearances(name, characters, appearance_lists)

    print("Converting all appearance_list contents to integer")
    for appearances_of_person in appearance_lists:
        for episode in range(len(appearances_of_person)):
            appearances_of_person[episode] = int(appearances_of_person[episode])

    console_print_char_and_apps(characters, appearance_lists)

main()
