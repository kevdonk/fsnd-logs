#!/usr/bin/env python
import psycopg2

DBNAME = "news"


def execute_query(query):
    """Execute sql query and return results"""
    try:
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print error


def get_popular_articles():
    """Return 3 articles with most views"""
    return execute_query("""SELECT title, count(articles.id)
                            FROM log, articles
                            WHERE log.path = '/article/' || slug
                            GROUP BY articles.id
                            ORDER BY count DESC
                            LIMIT 3;""")


def get_popular_authors():
    """Return 3 authors with most views"""
    return execute_query("""SELECT name, count(name)
                            FROM log, articles, authors
                            WHERE log.path = '/article/' || slug
                            AND author = authors.id
                            GROUP BY name
                            ORDER BY count DESC;""")


def get_high_error_rate_days():
    """Return days with > 1% error rate"""
    return execute_query("""WITH log_with_error_rate AS (
                                SELECT time ::timestamp::date,
                                (100.0 * sum(CASE WHEN status LIKE '4%'
                                OR status like '5%' THEN 1 ELSE 0 END)
                                / count(status))
                                AS error_rate
                                FROM log
                                GROUP BY time ::timestamp::date
                            )
                            SELECT time ::timestamp::date, error_rate
                            FROM log_with_error_rate
                            WHERE error_rate > 1.0
                            ORDER BY error_rate DESC;""")


def print_results(title, result):
    """Print a title, followed by a result with its view count"""
    print title
    for name, views in result:
        print '{}: {} views'.format(name, views)
    print "\n"


def print_high_error_days(days):
    """Print a title, followed by days with >1% error rate"""
    print "On which days did more than 1% of requests lead to errors?"
    for date, error_rate in days:
        print '{:%B %d %Y}: {:0.2f}%'.format(date, error_rate)


if __name__ == '__main__':
    article_title = "What are the most popular three articles of all time?"
    author_title = "Who are the most popular article authors of all time?"

    print_results(article_title, get_popular_articles())
    print_results(author_title, get_popular_authors())

    print_high_error_days(get_high_error_rate_days())
