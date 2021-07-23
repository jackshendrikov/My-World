import csv
from datetime import datetime
from movie_finder.models import Rate, Genre, Runtime, Type, Netflix, Year, Youtube, Movie


fhand = open('movies.csv', encoding='utf-8')
reader = csv.reader(fhand)
next(reader)

for row in reader:
    try:
        Movie.objects.get(imdb_id=row[0])
    except Movie.DoesNotExist:
        print(row)

        r, created = Rate.objects.get_or_create(rating=row[2])
        g, created = Genre.objects.get_or_create(genres=row[5])
        rt, created = Runtime.objects.get_or_create(runtime=row[7])
        t, created = Type.objects.get_or_create(mtype=row[8])
        n, created = Netflix.objects.get_or_create(netflix=row[9])
        y, created = Year.objects.get_or_create(year=row[13])
        yt, created = Youtube.objects.get_or_create(youtube=row[15])

        movie_date = datetime.strptime(row[12], '%d %b %Y').strftime('%Y-%m-%d')

        movie = Movie(imdb_id=row[0], title=row[1], rating=r, link=row[3], votes=row[4], genres=g, cast=row[6],
                      runtime=rt, mtype=t, netflix=n, plot=row[10], keywords=row[11], release=movie_date, year=y,
                      poster=row[14], youtube=yt)

        movie.save()

print('Done!')
exit()
