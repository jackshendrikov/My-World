from django.db import connection


def dump_queries():
    qs = connection.queries
    for q in qs:
        print(q)
