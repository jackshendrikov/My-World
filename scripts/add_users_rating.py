import csv
import re
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned

from movie_finder.models import Movie
from users.models import MyRating

count = 0
print('Started!')

# id, title, userId, rating
with open('users_rating.csv', 'r') as read_obj:
    reader = csv.reader(read_obj)
    next(reader)
    for row in reader:
        movie_title = re.split(r' \([0-9]{4}\)', row[1])[0]
        user_id = int(row[2])

        if (user_id,) in list(User.objects.all().values_list('id')) and Movie.objects.all().filter(title=movie_title).exists():
            try:
                movie_id = Movie.objects.all().get(title=movie_title).imdb_id
            except MultipleObjectsReturned:
                continue

            user_rating = int(float(row[3])) * 2

            MyRating(user_id=user_id, movie_id=movie_id, rating=user_rating).save()
            count += 1

            if count % 1000 == 0:
                print(count, 'new rows!')

print('Done')
