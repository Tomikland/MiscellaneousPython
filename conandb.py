'''A scraper to create a detective conan information db'''

__author__ = 'Mike'
import re
import requests
from bs4 import BeautifulSoup
from progress.bar import Bar

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

def find_latest_episode(the_appearance_lists):
    latest_ep = 0
    for each in the_appearance_lists:
        if max(each) > latest_ep:
            latest_ep = max(each)
    return latest_ep

def reverse_appearances(the_name, the_characters, the_appearance_lists):
    """Some characters, such as Conan, have lists of episodes in which they DON'T appear."""
    conan = the_characters.index(the_name)
    latest_ep = find_latest_episode(the_appearance_lists)
    episodes_with_conan = set(list(range(1, latest_ep+1)))
    the_appearance_lists[conan] = list(episodes_with_conan - set(the_appearance_lists[conan]))

def scrape_episode_data():
    pageurl = 'http://www.detectiveconanworld.com/wiki/Anime'

    html = requests.get(pageurl).text
    soup = BeautifulSoup(html, 'html.parser')

    #Constants for navigating cols
    EP_NUM = 1 #Japan
    ENG_EP_NUM = 2
    EP_NAME = 3
    AIRDATE = 4
    ENG_AIRDATE = 5
    # \n is the separater and there is always a \n here in the html
    PLOT = 7
    MANGA_SOURCE = 8
    HINT = 9

    ep_data = [None] # No zeroth episode
    for row in soup.find_all('tr'):
        cols = row.get_text().split("\n")

        # Not a data row
        if not cols[EP_NUM].strip().isdigit():
            continue

        if int(cols[EP_NUM]) > len(ep_data)-1: # Not a rerun
            ep = dict()
            ep["jp_num"] = int(cols[EP_NUM].strip())
            ep["name"] = cols[EP_NAME].strip()
            ep_data.append(ep)
        else: # A rerun
            continue
            
    return ep_data

def scrape_character_data():
    print("Getting characters")
    characters = get_characters()
    appearance_lists = []
    bar = Bar('Extracting appearances...', max=len(characters), suffix='%(percent)d%%')
    for person in characters:
        html = requests.get(URL_START + person + PAGE_URL_END).text
        start = html.find(r'=edit&amp;section=2')
        end = html.find('/table', start)
        episodes_str = re.findall(r"<li>.+<b>Episode (.+?)</b>", html[start:end])
        episodes = []
        for ep in episodes_str:
            if not ep.isdigit():
                ep = re.sub(r"([^\d]+)", r"", ep)
            episodes.append(int(ep))
        appearance_lists.append(episodes)
        bar.next()
    bar.finish()

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

    print("Reversing Characters")
    chars_needing_reverse = ["Conan Edogawa", "Ran Mouri", "Kogoro Mouri"]
    for name in chars_needing_reverse:
        reverse_appearances(name, characters, appearance_lists)

    print("Converting all appearance_list contents to integer")
    for appearances_of_person in appearance_lists:
        for episode in range(len(appearances_of_person)):
            appearances_of_person[episode] = int(appearances_of_person[episode])

    # console_print_char_and_apps(characters, appearance_lists)
    
    return characters, appearance_lists

def create_episode_objects(characters, appearance_lists, episode_data):
    episodes = dict()
    bar = Bar('Creating episode structure...', max=len(characters), suffix='%(percent)d%%')
    for each_episode in range(1, find_latest_episode(appearance_lists)):
        # Create a row in table
        episodes[each_episode] = {"name":"", "characters":[]}
        episodes[each_episode]["name"] = episode_data[each_episode]["name"]
        # Create the array of characters appearing in the episode
        for each_character in range(len(appearance_lists)):
            if each_episode in appearance_lists[each_character]:
                episodes[each_episode]["characters"].append(each_character)
        bar.next()
    bar.finish()
    return episodes

def main():
    characters, appearance_lists = scrape_character_data()

    episode_data = scrape_episode_data()

    episodes = create_episode_objects(characters, appearance_lists, episode_data)

    with open("out.txt", "w") as f:
        f.write(str(episodes))

    with open("names.txt", "w") as f:
        for character_id in range(len(characters)):
            f.write(str(character_id) + " " + characters[character_id] + "\n")

main()
