from os import path, walk, remove
from re import sub, search

for dirpath, dirnames, filenames in walk("../staticfiles/"):
    for filename in [f for f in filenames if bool(search(r'.[0-9a-f]{12}', f))]:
        remove(path.join(dirpath, filename))

fhandler = '../staticfiles/staticfiles.json'

with open(fhandler, "r") as f:
    data = f.read()

with open(fhandler, "w") as f:
    f.write(sub(r'.[0-9a-f]{12}', '', data))

print('Done!')
