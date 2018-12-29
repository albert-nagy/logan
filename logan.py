#!/usr/bin/env python2

import psycopg2
from datetime import datetime

db = psycopg2.connect(dbname='news')
c = db.cursor()

print("\nThe 3 most popular articles of all time:\n")

c.execute("""
SELECT title, num
FROM articles,
(SELECT path, COUNT(id) AS num FROM log WHERE status LIKE '2%'
GROUP BY path) lg
WHERE path = CONCAT('/article/',slug)
ORDER BY num DESC LIMIT 3;
""")

most_viewed = c.fetchall()

for article in most_viewed:
    print('"{}" - {} views'.format(article[0], article[1]))

print("\nThe most popular authors of all time:\n")

c.execute("""
SELECT name, SUM(num) AS all_views
FROM articles, authors au,
(SELECT path, COUNT(id) AS num
FROM log  WHERE status LIKE '2%' GROUP BY path) lg
WHERE path = CONCAT('/article/',slug) AND au.id = author
GROUP BY name ORDER BY all_views DESC;
""")

most_popular = c.fetchall()

for author in most_popular:
    print('"{}" - {} views'.format(author[0], author[1]))

print("\nOn which days did more than 1% of the requests lead to errors?\n")

c.execute("""
SELECT e.day, (e404 * 100) / views::float
FROM
(SELECT COUNT(*) AS e404, time::timestamptz::date AS day
FROM log WHERE status LIKE '4%' OR status LIKE '5%' GROUP BY day) e,
(SELECT COUNT(*) AS views, time::timestamptz::date AS day
FROM log GROUP BY day) av
WHERE e.day = av.day AND e404 / views::float > 0.01
ORDER BY e404 DESC;
""")

days_of_error = c.fetchall()

for days in days_of_error:
    print(
        "{} - {}% errors".format(
            datetime.strftime(
                days[0], '%d %B, %Y'), round(
                days[1], 1)))

db.close()
