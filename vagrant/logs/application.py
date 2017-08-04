#!/usr/bin/env python
import psycopg2

DBNAME = "news"

def get_popular_articles():
    """Return 3 articles with most views"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT title, count(articles.id) FROM log, articles WHERE log.path LIKE TEXTCAT('/article/', articles.slug) GROUP BY articles.id ORDER BY count DESC LIMIT 3;")
    articles = c.fetchall()
    db.close()
    return articles

def get_popular_authors():
    """Return 3 authors with most views"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT name, count(name) FROM log, articles, authors WHERE log.path LIKE TEXTCAT('/article/', articles.slug) AND author = authors.id GROUP BY name ORDER BY count DESC;")
    authors = c.fetchall()
    db.close()
    return authors

def get_high_error_rate_days():
    """Return days with > 1% error rate"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT time ::timestamp::date, (100.0 * sum(CASE WHEN status LIKE '4%' OR status like '5%' THEN 1 ELSE 0 END) / count(status)) AS error_rate FROM log GROUP BY time ::timestamp::date ORDER BY error_rate DESC;")
    days = c.fetchall()
    db.close
    return days
    

def print_results(title, result):
    """Print a title, followed by a result with its view count"""
    print title
    for result in result:
        print result[0] + ": " + str(result[1]) + " views"
    print "\n"

def print_high_error_days(days):
    """Print a title, followed by days with >1% error rate"""
    print "On which days did more than 1% of requests lead to errors?"
    for day in days:
        if day[1] > 1.00:
            print str(day[0]) + ": " + str(day[1]) + "%"

article_title = "What are the most popular three articles of all time?"
author_title = "Who are the most popular article authors of all time?"

print_results(article_title, get_popular_articles())
print_results(author_title, get_popular_authors())

print_high_error_days(get_high_error_rate_days())