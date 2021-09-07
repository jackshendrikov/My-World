import csv
import requests

from datetime import datetime
from movie_finder.models import Rate, Genre, Runtime, Type, Netflix, Year, Youtube, Movie
from jackshen.settings import SHEET_ID
from home.utils.check_progress import print_progress

url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=904865657'

with requests.Session() as s:
    decoded_content = s.get(url).content.decode('utf-8')

    reader = csv.reader(decoded_content.splitlines(), delimiter=',')
    next(reader)

    reader = list(reader)
    l = len(reader)

    print('Started..')
    print_progress(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, row in enumerate(reader):
        r, created = Rate.objects.get_or_create(rating=row[2])
        votes = row[4]
        cast = row[6]
        kw = row[11]
        yt, created = Youtube.objects.get_or_create(youtube=row[15])

        if Movie.objects.filter(imdb_id=row[0]).exists():
            Movie.objects.filter(imdb_id=row[0]).update(rating=r, votes=votes, cast=cast, keywords=kw, youtube=yt)
        else:
            g, created = Genre.objects.get_or_create(genres=row[5])
            rt, created = Runtime.objects.get_or_create(runtime=row[7])
            t, created = Type.objects.get_or_create(mtype=row[8])
            n, created = Netflix.objects.get_or_create(netflix=row[9])
            y, created = Year.objects.get_or_create(year=row[13])

            movie_date = datetime.strptime(row[12], '%d %b %Y').strftime('%Y-%m-%d')

            Movie(imdb_id=row[0], title=row[1], rating=r, link=row[3], votes=votes, genres=g, cast=cast,
                  runtime=rt, mtype=t, netflix=n, plot=row[10], keywords=kw, release=movie_date, year=y,
                  poster=row[14], youtube=yt).save()

        print_progress(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

    print('Done!')
    exit()
