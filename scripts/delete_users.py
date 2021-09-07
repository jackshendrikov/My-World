from django.contrib.auth.models import User


def run(*script_args):

    if len(script_args) == 2:
        try:
            start, end = int(script_args[0]), int(script_args[1])

            print('Started!')
            for i in range(start, end):
                try:
                    User.objects.get(username='test' + str(i)).delete()
                except User.DoesNotExist:
                    continue
            print('Done!')
        except ValueError:
            exit('Enter valid args!')
    else:
        print('Enter valid args!')
