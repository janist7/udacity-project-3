"""Gets data for report"""

import datetime
import psycopg2

DBNAME = "news"

def get_reports():
  result = []

  db = psycopg2.connect(database=DBNAME)
  cursor = db.cursor()

  cursor.execute(
    """SELECT title, num || ' views'
    FROM articles,
        (SELECT path, count(path) as num
        FROM log
        WHERE status = '200 OK'
        AND path <> '/'
        GROUP BY path) as logs
    WHERE path = concat('/article/',slug)
    GROUP BY title, num
    ORDER BY num DESC
    LIMIT 3;
    """)
  result.append(
    {"title":"What are the most popular three articles of all time?",
    "answer":cursor.fetchall()}
  )
  """
  Use one view for formmating:

  CREATE VIEW popular_article_authors AS SELECT name as author_name, count(logs_sub.path) as author_views
    FROM articles,authors,
        (SELECT path
        FROM log
        WHERE status = '200 OK'
        AND path <> '/') as logs_sub
    WHERE logs_sub.path = concat('/article/',slug)
    AND author = authors.id
    GROUP BY name
    ORDER BY author_views DESC;

  """
  cursor.execute(
    """SELECT author_name, author_views || ' views'
    FROM popular_article_authors;
    """)
  result.append(
    {"title":"Who are the most popular article authors of all time?",
    "answer":cursor.fetchall()}
  )
  """
  Uses 3 views to get result:

  CREATE VIEW log_day AS SELECT TO_CHAR(time,'Month DD, YYYY') as f_time_day,count(status) as num_day 
        FROM log
        WHERE status <> '200 OK' 
        AND path <> '/'
        GROUP BY f_time_day;

  CREATE VIEW log_all AS SELECT TO_CHAR(time,'Month DD, YYYY') as f_time_all,count(status) as num_all 
        FROM log 
        GROUP BY f_time_all;

  CREATE VIEW error_percent AS SELECT f_time_day as day,trunc(CAST(num_day AS DECIMAL)/CAST(num_all AS DECIMAL)*100,2) as percent
    FROM log_day,log_all
    WHERE f_time_day = f_time_all
    GROUP BY f_time_day,num_day,num_all
    ORDER BY percent DESC;
  """
  cursor.execute(
    """SELECT day, percent || '% errors'
    FROM error_percent
    WHERE percent > 1;
    """)
  result.append(
    {"title":"On which days did more than 1% of requests lead to errors? ",
    "answer":cursor.fetchall()}
  )
  
  db.close
  return result
  
  
  


