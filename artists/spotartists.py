import spotipy
import csv
import re

from util import ARTISTS, get_artist_id


instance = spotipy.Spotify()

def get_data():
    artist_ids = []
    for name in ARTISTS:
        print(name)
        result = get_artist_id(instance, name)
        if result:
            artist_ids.append(result)

    artist_data = [instance.artist(artist_id) for artist_id in artist_ids]
    return artist_data

def dict_to_csv(data):
    with open(r'C:\Users\1324172\Documents\QlikProjects\Music\0DataSource\artists.csv',
              'w', newline='') as f:
        
        fieldnames = ['id', 'name', 'image', 'popularity', 'followers']
        writer = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        writer.writeheader()
        for artist in data:
            if artist['images']:
                artist['image'] = artist['images'][0]['url']
            else:
                artist['image'] = 'https://dummyimage.com/100x100/000000/ffffff&text={}'.format(re.sub(' ', '+', artist['name']))
            artist['followers'] = artist['followers']['total']
            writer.writerow(artist)

    with open(r'C:\Users\1324172\Documents\QlikProjects\Music\0DataSource\genres.csv',
              'w', newline='') as g:
        fieldnames = ['id', 'genre']
        writer = csv.DictWriter(g, fieldnames, extrasaction='ignore')
        writer.writeheader()
        items = []
        for artist in data:
            for genre in artist['genres']:
                writer.writerow({'id':artist['id'], 'genre':genre})

def main():
    dict_to_csv(get_data())

if __name__ == '__main__':
    main()
