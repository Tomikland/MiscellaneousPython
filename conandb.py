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
    print(the_appearance_lists[conan])
    latest_ep = 0
    for each in the_appearance_lists:
        if max(each) > latest_ep:
            latest_ep = max(each)
    episodes_with_conan = set(list(range(1, latest_ep+1)))
    the_appearance_lists[conan] = list(episodes_with_conan - set(the_appearance_lists[conan]))

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
        episodes_str = re.findall(r"<li>.+<b>Episode (.+?)</b>", html[start:end])
        episodes = []
        for ep in episodes_str:
            if not ep.isdigit():
                ep = re.sub(r"([^\d]+)", r"", ep)
                print("CHANGED", ep) 
            episodes.append(int(ep))
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
