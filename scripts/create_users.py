from django.contrib.auth.models import User
from decouple import config

user_len = User.objects.all().count()

for i in range(user_len, user_len+100):
    user_num = 'test' + str(i)
    User.objects.create_user(username=user_num,
                             email=user_num+'@gmail.com',
                             password=config('TEST_PASSWORD'))

print('Done!')
