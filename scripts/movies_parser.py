import json
import ssl
from imdb import IMDb
import urllib.request
from movie_finder.settings import OMDB_KEY

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

new_movies = open('new_movies.txt', 'r').readlines()
all_movies = open('../movies.csv', 'a', encoding='utf-8')
ia = IMDb()

for imdb_id in new_movies:
    data_URL = 'https://www.omdbapi.com/?i=' + imdb_id.strip() + '&apikey=' + OMDB_KEY
    print('-' * 70 + '\nRetrieving:', data_URL)

    json_data = urllib.request.urlopen(data_URL).read().decode()
    print('Retrieved', len(json_data), 'characters')

    keywords = ia.get_movie(imdb_id.strip()[2:], info='keywords')

    data = json.loads(json_data)
    # imdb_id, title, rating, link, votes, genre, cast, runtime, type,
    # netflix, plot, keywords, release, year, poster, youtube
    all_movies.write('\n' +
                     data["imdbID"] + ',"' + data["Title"] + '",' + data["imdbRating"] + ',https://www.imdb.com/title/' +
                     data["imdbID"] + ',' + data["imdbVotes"].replace(',', '') + ',"' + data["Genre"] + '","' +
                     str(data["Actors"].replace("'", "`").split(', ')) + '",' + data["Runtime"].split()[0] + ',' +
                     data["Type"].title() + ',None,"' + data["Plot"].replace('"', "'") + '","' + ", ".join(keywords['keywords'][:15]) +
                     '",' + data["Released"] + ',' + data["Year"].split('–')[0] + ',' + data["Poster"] + ',None')

all_movies.close()
