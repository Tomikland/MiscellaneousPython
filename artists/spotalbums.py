import spotipy
import csv
import re
import os

from util import ARTIST_IDS, get_artist_id


instance = spotipy.Spotify()

def ensure_image(dic):
    if dic['images']:
        dic['image'] = dic['images'][-1]['url'] #-1 is smallest image
    else:
        dic['image'] = 'https://dummyimage.com/100x100/000000/ffffff&text={}'.format(re.sub(' ', '+', dic['name']))

def process_artists(data):
    print('Processing Artists')
    try:
        os.remove(r'..\artists.csv')
        os.remove(r'..\genres.csv')
    except:
        pass

    artist_data = [instance.artist(artist_id) for artist_id in ARTIST_IDS]

    with open(r'C:\Users\1324172\Documents\QlikProjects\Music\0DataSource\artists.csv',
              'w', newline='') as f:
        
        fieldnames = ['id', 'name', 'image', 'popularity', 'followers']
        writer = csv.DictWriter(f, fieldnames, encoding='UTF-8', extrasaction='ignore')
        writer.writeheader()
        for artist in data:
            ensure_image(artist)
            artist['followers'] = artist['followers']['total']
            writer.writerow(artist)

    with open(r'C:\Users\1324172\Documents\QlikProjects\Music\0DataSource\genres.csv',
              'w', newline='') as g:
        fieldnames = ['id', 'genre']
        writer = csv.DictWriter(g, fieldnames, encoding='UTF-8', extrasaction='ignore')
        writer.writeheader()
        items = []
        for artist in data:
            for genre in artist['genres']:
                writer.writerow({'id':artist['id'], 'genre':genre})

#Side effect: expands ARTISTS for artists sharing albums.
def process_albums():
    print('Processing Albums')
    try:
        os.remove(r'..\albums.csv')
        os.remove(r'..\available_markets.csv')
        os.remove(r'..\artist_to_album.csv')
    except:
        pass
    
    for i, artist_id in enumerate(ARTIST_IDS):
        print(i+1, 'of', len(ARTIST_IDS))

        albums = instance.artist_albums(artist_id)['items']

        with open(r'..\albums.csv', 'a', encoding='UTF-8', newline='') as albumfile:
            fieldnames =['album_id', 'album_type', 'name', 'image']

            writer = csv.DictWriter(albumfile, fieldnames, extrasaction='ignore')
            writer.writeheader()

            for album in albums:
                ensure_image(album)
                album['album_name'] = album['name']
                album['album_id'] = album['id']

                writer.writerow(album)

        #Also create available market csv
        with open(r'..\available_markets.csv', 'a', encoding='UTF-8', newline='') as marketfile:
            fieldnames =['album_id', 'available_markets']
            writer = csv.DictWriter(marketfile, fieldnames, extrasaction='ignore')
            writer.writeheader()

            for album in albums:
                for market in album['available_markets']:
                    writer.writerow({'album_id':album['id'], 'available_markets':market})

        #Also create link table for artists to album
        with open(r'..\artist_to_album.csv', 'a', encoding='UTF-8', newline='') as marketfile:
            fieldnames =['album_id', 'artist_id']
            writer = csv.DictWriter(marketfile, fieldnames, extrasaction='ignore')
            writer.writeheader()

            for album in albums:
                for artist in album['artists']:
                    writer.writerow({'album_id':album['id'], 'artist_id':artist['id']})

def populate_artists():
    for i, artist_id in enumerate(ARTIST_IDS):
        print(i+1, 'of', len(ARTIST_IDS))
        if len(ARTIST_IDS) > 10000:
            break
        
        albums = instance.artist_albums(artist_id)['items']
        
        for album in albums:
            for artist in album['artists']:
                if artist['id'] not in ARTIST_IDS:
                    ARTIST_IDS.append(artist['id'])
    with open('artist.dat', 'w') as f:            
        for artist_id in ARTIST_IDS:
            f.write(artist_id + '\n')
            
populate_artists()
process_albums() #Important that albums is first
process_artist(get_artist_data())

