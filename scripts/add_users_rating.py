import csv
import re
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from movie_finder.models import Movie
from users.models import MyRating
from home.utils.check_progress import print_progress

print('Started!')

# id, title, userId, rating
with open('users_rating.csv', 'r') as read_obj:
    reader = csv.reader(read_obj)
    next(reader)

    reader = list(reader)
    l = len(reader)

    print_progress(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, row in enumerate(reader):
        movie_title = re.split(r' \([0-9]{4}\)', row[1])[0]
        user_id = int(row[2])

        if (user_id,) in list(User.objects.all().values_list('id')) and Movie.objects.all().filter(title=movie_title).exists():
            try:
                movie_id = Movie.objects.all().get(title=movie_title).imdb_id
            except MultipleObjectsReturned:
                continue

            user_rating = int(float(row[3])) * 2

            MyRating(user_id=user_id, movie_id=movie_id, rating=user_rating).save()

        print_progress(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

print('Done')
