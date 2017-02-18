import csv
import re
import requests
from bs4 import BeautifulSoup

YEAR_TO_EXTENSION = {1986:"1st",1987:"2nd",1988:"3rd",1989:"4th",1990:"5th",
                     1991:"6th",1992:"7th",1993:"8th",1994:"9th",1995:"10th",
                     1996:"11th",1997:"12th",1998:"13th",1999:"14th",2000:"15th",
                     2001:"16th",2002:"17th",2003:"18th",2004:"19th",2005:"20th",
                     2006:"21st",2007:"22nd",2008:"23rd",2009:"24th",2010:"25th",
                     2011:"26th",2012:"27th",2013:"28th",2014:"29th",2015:"30th",
                     2016:"31st"}

#Some awards give the movie name first, then the winner.
#These need to be detected, and swapped manually. Unfortunately.
AWARDS_WITH_FLIPPED_WINNERS = {"Best Original Screenplay", "Best Adapted Screenplay",
                               "Best Spanish Language Foreign Film", "Best European Film",
                               "Best New Director", "Best Screenplay", "Original Screenplay",
                               "Adapted Screenplay"}

#Global count of the number of nominations, used to identify specific nominations.
nomination_id = 1

def get_nominees(table):
    #The runner up ul is nested in the winner ul.
    #Look at every other result, skipping the copies caused by this.
    nominee_groups = table.find_all("ul")[::2]

    #Extract the text information from the li entries in the ul
    for index, group in enumerate(nominee_groups):
        nominee_groups[index] = [nominee.text for nominee in group.find_all('li')]

    #The runners up are in li nested within the winner's ul.
    #This next loop processes:
    #    Voyage to Nowhere\n\n27 Hours\nHalf of Heaven\n\n
    #to
    #    Voyage to Nowhere
    for group in nominee_groups:
        if len(group) > 1: #Some winners were unopposed, though.
            group[0] = group[0][:group[0].find('\n')]


    #Note that the winner is always the zeroth entry in a group
    return nominee_groups

def get_awards(table):
    return [award.text for award in table.find_all("th")]

separator_regex = re.compile(" –|–|• ")
def split_nominee(raw_nominee, award_name):
    parts = separator_regex.split(raw_nominee)

    if award_name in AWARDS_WITH_FLIPPED_WINNERS:
        parts.reverse()

    winner = parts[0] if len(parts) > 1 else None

    #The winner can be the movie itself. There is no separator in that case.
    movie = parts[1] if len(parts) > 1 else parts[0]
    
    return winner, movie

def process_movie(year, movie_extension):
    page = requests.get("https://en.wikipedia.org/wiki/" + movie_extension + '_Goya_Awards')

    soup = BeautifulSoup(page.text, 'html.parser')

    tables = soup.find_all("table", class_="wikitable")

    for table in tables: #TODO: The minor awards aren't showing
        
        nominee_groups = get_nominees(table)
    
        awards = get_awards(table)
        
        awards_with_nominees = list(zip(awards, nominee_groups))

        results = []
        
        global nomination_id

        for award, nominees in awards_with_nominees:
            #write winner
            winner_name, movie_name = split_nominee(nominees[0], award)
            results.append({"nomination_id":nomination_id, "award":award, "name":winner_name,
                            "is_winner":"Winner", "movie":movie_name, "year":year})

            nomination_id += 1
            
            #write other nominees. [1:] to cut off winner.
            for nominee in nominees[1:]:
                nominee_name, movie_name = split_nominee(nominee, award)
                results.append({"nomination_id":nomination_id, "award":award, "name":nominee_name,
                                "is_winner":"Nominated", "movie":movie_name, "year":year})
                nomination_id += 1
                
        return results


def main():
    #TODO: NamedTuple would be better than the dict
    with open('goyaawards.csv', 'w') as file:
        fieldnames = 'nomination_id', 'year', 'award', 'name', 'is_winner', 'movie'
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for year in YEAR_TO_EXTENSION:
            results = process_movie(year, YEAR_TO_EXTENSION[year])
            for row in results:
                writer.writerow(row)
            print(year, 'finished')
            
if __name__ == '__main__':
    main()
