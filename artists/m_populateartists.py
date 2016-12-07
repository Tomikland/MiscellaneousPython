from m_util import ARTIST_IDS

def populate_artists():
    for i, artist_id in enumerate(ARTIST_IDS):
        print(i+1, 'of', len(ARTIST_IDS))
        if len(ARTIST_IDS) > 1000:
            break
        
        albums = instance.artist_albums(artist_id)['items']
        
        for album in albums:
            for artist in album['artists']:
                if artist['id'] not in ARTIST_IDS:
                    ARTIST_IDS.append(artist['id'])
    with open('m_artist.dat', 'w') as f:            
        for artist_id in ARTIST_IDS:
            f.write(artist_id + '\n')
            
if __name__ == '__main__':
    populate_artists()
