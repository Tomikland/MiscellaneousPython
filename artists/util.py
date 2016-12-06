import sys

ARTISTS = ['Tony Allen', 'George Clinton', 'Zakir Hussain',
           'Johnny Pacheco', 'Charles Aznavour', 'Ry Cooder',
           'B.B. King', 'Dolly Parton', 'Harry Belafonte',
           'James Cotton', 'Carole King', 'Iggy Pop',
           'Tony Bennett', 'Danger Mouse', 'Kool Herc',
           'Prince', 'Chuck Berry', 'Dr. Dre', 'Little Richard',
           'Prince Buster', 'Beyoncé', 'Dr. John', 'Madonna',
           'A.R. Rahman', 'Jay-Z', 'Bob Dylan', 'Paul McCartney',
           'Smokey Robinson', 'Bono', 'Aretha Franklin',
           'Giorgio Moroder', 'Nile Rodgers', 'David Bowie',
           'Joao Gilberto', 'Ennio Morricone', 'Bruce Springsteen',
           'Garth Brooks', 'Philip Glass', 'Nana Mouskouri',
           'Tina Turner', 'David Byrne', 'Dave Grohl',
           'Youssou N\'Dour', 'Caetano Veloso', 'Ron Carter',
           'Herbie Hancock', 'Willie Nelson', 'Neil Young',
           'Jimmy Cliff', 'Ozzy Osbourne']

ARTIST_IDS = ['6JpZEemWmunccsrHXFUOgi', '2GVBp7QyHckoOg7rYkLvrA',
              '6DDCjHWtL6jTl1B5wG8tF6', '09947uhj2ZwU9mFXK5v50o',
              '2hgP9Ap2tc10R5jrQaEpMT', '1CPwHx5lgVxv0rfcp7UXLx',
              '5xLSa7l4IV1gsQfhAMvl0U', '32vWCbZh0xZ4o9gkz4PsEU',
              '6Tw1ktF4xMmzaLLbe98I2z', '6mY93oNfUaUwZq67yn3R8k',
              '319yZVtYM9MBGqmSQnMyY6', '33EUXrFKGjpUSGacqEHhU4',
              '2lolQgalUvZDfp5vvVtTYV', '2dBj3prW7gP9bCCOIQeDUf',
              '0VcTIm4tmf91b3mWd8lVuQ', '3MHaV05u0io8fQbZ2XPtlC',
              '293zczrfYafIItmnmM3coR', '6DPYiyq5kWVQS4RGwxzPC7',
              '4xls23Ye9WR9yy3yYMpAMm', '75S63f1AmZUa9gpQvlt5NB',
              '6vWDO969PvNqNYHIOW5v0m', '320TrJub4arztwXRm7kqVO',
              '6tbjWDEIzxoDsBA1FuhfPW', '1mYsTxnqsietFxj1OgoGbG',
              '3nFkdlSjzX9mRTtwJOzDYB', '74ASZWbe4lXaubB36ztrGX',
              '4STHEaNw4mPZ2tzheohgXB', '6TKOZZDd5uV5KnyC5G4MUt',
              '0m2Wc2gfNUWaAuBK7URPIJ', '7nwUJBm0HE4ZxD3f5cy5ok',
              '6jU2Tt13MmXYk0ZBv1KmfO', '3yDIp0kaq9EFKe07X1X2rz',
              '0oSGxfWSnnOXhD2fKuz2Gy', '77ZUbcdoU5KCPHNUl8bgQy',
              '1nIUhcKHnK6iyumRyoV68C', '3eqjTLE0HfPfh78zjh6TqT',
              '4BclNkZtAUq1YrYNzye3N7', '69lxxQvsfAIoQbB20bEPFC',
              '6p7iFdv6Wn9iaS7AwVLvod', '1zuJe6b1roixEKMOtyrEak',
              '20vuBdFblWUo2FCOvUzusB', '7mRVAzlt1fAAR9Cut6Rq8c',
              '77zlytAFjPFjUKda8TNIDY', '7HGNYPmbDrMkylWqeFCOIQ',
              '4wnzivx3OQ3vjrySAdTdJP', '2ZvrvbQNrHKwjT7qfGFFUW',
              '5W5bDNCqJ1jbCgTxDD0Cb3', '6v8FB84lnmJs434UJf2Mrm',
              '3rJ3m1tM6vUgiWLjfV8sRf', '6ZLTlhejhndI4Rh53vYhrY']

def get_artist_id(instance, name):
    try:
        results = instance.search(q='artist:' + name, type='artist')
        return results['artists']['items'][0]['id']
    except:
        print(name, "didn't work:", sys.exc_info()[0])
        return None
