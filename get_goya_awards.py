import csv
import re
import requests
from bs4 import BeautifulSoup

YEAR_TO_EXTENSION = {1986:"1st_Goya_Awards",
1987:"2nd_Goya_Awards",
1988:"3rd_Goya_Awards",
1989:"4th_Goya_Awards",
1990:"5th_Goya_Awards",
1991:"6th_Goya_Awards",
1992:"7th_Goya_Awards",
1993:"8th_Goya_Awards",
1994:"9th_Goya_Awards",
1995:"10th_Goya_Awards",
1996:"11th_Goya_Awards",
1997:"12th_Goya_Awards",
1998:"13th_Goya_Awards",
1999:"14th_Goya_Awards",
2000:"15th_Goya_Awards",
2001:"16th_Goya_Awards",
2002:"17th_Goya_Awards",
2003:"18th_Goya_Awards",
2004:"19th_Goya_Awards",
2005:"20th_Goya_Awards",
2006:"21st_Goya_Awards",
2007:"22nd_Goya_Awards",
2008:"23rd_Goya_Awards",
2009:"24th_Goya_Awards",
2010:"25th_Goya_Awards",
2011:"26th_Goya_Awards",
2012:"27th_Goya_Awards",
2013:"28th_Goya_Awards",
2014:"29th_Goya_Awards",
2015:"30th_Goya_Awards",
2016:"31st_Goya_Awards"}

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
#TODO: Certain awards are reversed.
#Just have to pass in the category and detect manually
def split_nominee(raw_nominee):
    parts = separator_regex.split(raw_nominee)

    winner = parts[0]

    #The winner can be the movie itself. There is no separator in that case.
    movie = parts[1] if len(parts) > 1 else parts[0]
    
    return winner, movie

def process_movie(year, movie_extension):
    page = requests.get("https://en.wikipedia.org/wiki/" + movie_extension)

    soup = BeautifulSoup(page.text, 'html.parser')

    tables = soup.find_all("table", class_="wikitable")

    for table in tables: #TODO: The minor awards aren't showing
        
        nominee_groups = get_nominees(table)
    
        awards = get_awards(table)
        
        awards_with_nominees = list(zip(awards, nominee_groups))

        
        results = []
        for award, nominees in awards_with_nominees:
            #write winner
            winner_name, movie_name = split_nominee(nominees[0])
            results.append({"award":award, "name":winner_name, 'winner':'Yes',
                         "movie":movie_name, "year":year})
            
            #write other nominees. [1:] to cut off winner.
            for nominee in nominees[1:]:
                nominee_name, movie_name = split_nominee(nominee)
                results.append({"award":award, "name":nominee_name, 'winner':'Yes',
                             "movie":movie_name, "year":year})
        return results


def main():
    #TODO: NamedTuple would be better than the dict
    with open('goyaawards.csv', 'w') as file:
        fieldnames = 'award', 'name', 'winner', 'movie', 'year'
        writer = csv.DictWriter(file, fieldnames=fieldnames, lineterminator='\n')
        for year in YEAR_TO_EXTENSION:
            results = process_movie(year, YEAR_TO_EXTENSION[year])
            for row in results:
                writer.writerow(row)
            print(year, 'finished')
            
if __name__ == '__main__':
    main()
