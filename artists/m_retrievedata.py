import spotipy
import csv
import re
import os

from m_util import ARTIST_IDS, get_artist_id

A_IDS = [artist_id.rstrip() for artist_id in open('m_artist.dat', 'r').readlines()[:1000]]

instance = spotipy.Spotify()

def ensure_image(dic):
    if dic['images']:
        dic['image'] = dic['images'][-1]['url'] #-1 is smallest image
    else:
        dic['image'] = 'https://dummyimage.com/100x100/000000/ffffff&text={}'.format(re.sub(' ', '+', dic['name']))

def process_artists():
    print('Processing Artists')
    try:
        os.remove(r'..\artists.csv')
        os.remove(r'..\genres.csv')
    except:
        pass

    data = [instance.artist(artist_id) for artist_id in A_IDS]

    with open(r'C:\Users\1324172\Documents\QlikProjects\Music\0DataSource\artists.csv',
              'w', encoding='UTF-8', newline='') as f:
        
        fieldnames = ['artist_id', 'name', 'image', 'popularity', 'followers']
        writer = csv.DictWriter(f, fieldnames, extrasaction='ignore')
        writer.writeheader()
        for i, artist in enumerate(data):
            print(i+1, 'of', len(data))
            ensure_image(artist)
            artist['followers'] = artist['followers']['total']
            artist['artist_id'] = artist['id']
            
            writer.writerow(artist)

    with open(r'C:\Users\1324172\Documents\QlikProjects\Music\0DataSource\genres.csv',
              'w', encoding='UTF-8', newline='') as g:
        fieldnames = ['artist_id', 'genre']
        writer = csv.DictWriter(g, fieldnames, extrasaction='ignore')
        writer.writeheader()
        items = []
        for i, artist in enumerate(data):
            print(i+1, 'of', len(data))
            for genre in artist['genres']:
                writer.writerow({'artist_id':artist['id'], 'genre':genre})

#Side effect: expands ARTISTS for artists sharing albums.
def process_albums():
    print('Processing Albums')
    try:
        os.remove(r'..\albums.csv')
        os.remove(r'..\available_markets.csv')
        os.remove(r'..\artist_to_album.csv')
    except:
        pass
    
    for i, artist_id in enumerate(A_IDS):
        print(i+1, 'of', len(A_IDS))
        artist_id = artist_id.rstrip()
        
        albums = instance.artist_albums(artist_id)['items']

        with open(r'..\albums.csv', 'a', encoding='UTF-8', newline='') as albumfile:
            fieldnames =['album_id', 'album_type', 'name', 'image']

            writer = csv.DictWriter(albumfile, fieldnames, extrasaction='ignore')
            if i == 0:
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
            if i == 0:
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
if __main__ == '__main__':
    process_albums()
    process_artists()

