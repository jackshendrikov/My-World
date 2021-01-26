from re import sub

fhandler = '../staticfiles/staticfiles.json'

with open(fhandler, "r") as f:
    data = f.read()

with open(fhandler, "w") as f:
    f.write(sub(r'.[0-9a-f]{12}', '', data))

print('Done!')
