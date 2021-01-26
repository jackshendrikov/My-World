import csv
from unesco.models import ISO, Category, Region, States, Site


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)
    next(reader)

    ISO.objects.all().delete()
    Category.objects.all().delete()
    Region.objects.all().delete()
    States.objects.all().delete()
    Site.objects.all().delete()

    for row in reader:
        print(row)

        c, created = Category.objects.get_or_create(name=row[7])
        s, created = States.objects.get_or_create(name=row[8])
        r, created = Region.objects.get_or_create(name=row[9])
        i, created = ISO.objects.get_or_create(name=row[10])

        lg, lt= row[4], row[5]

        try: j = row[2]
        except: j = None

        try: y = int(row[3])
        except: y = None

        for val in [lg, lt]:
            try: float(val)
            except: val = None

        if row[6] == '': ah = None
        else: ah = float(row[6])

        site = Site(
            name=row[0], description=row[1], justification=j,
            year=y, longitude=lg, latitude=lt, area_hectares=ah,
            category=c, states=s, region=r, iso=i
        )

        site.save()
