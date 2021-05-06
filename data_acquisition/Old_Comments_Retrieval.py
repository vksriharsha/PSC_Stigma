import praw
from psaw import PushshiftAPI
import pandas as pd
import datetime as dt
import pymysql

reddit = praw.Reddit(
    client_id="V08Pn1YEXyjTvw",
    client_secret="-n7x3ejKJQ3ewO2Dc_Cxx596_dWTdA",
    user_agent="crawler_01"
)

api = PushshiftAPI(reddit)

start_epoch=int(dt.datetime(2015, 12, 1).timestamp())
end_epoch=int(dt.datetime(2016, 1, 1).timestamp())

a = list(api.search_comments(after=start_epoch,
                             before=end_epoch,
                            subreddit='cripplingalcoholism'))

columns = ['body','author', 'created_utc', 'subreddit_id',
               'link_id', 'parent_id', 'score', 'id',
               'subreddit', 'distinguished']
data = []

try:

    # create connection
    connection = pymysql.connect(host='localhost',
                             user='root',
                             db='psc_stigma')

    # Create cursor
    my_cursor = connection.cursor()

    stmt = "INSERT INTO reddit_comments (body, author, created_utc, subreddit_id,link_id, parent_id, score, id,subreddit, distinguished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    for comment in a:
        data.append((comment.body, comment.author, comment.created_utc, comment.subreddit_id,
              comment.link_id, comment.parent_id, comment.score, comment.id,
              comment.subreddit.name, comment.distinguished))


    # Execute Query
    my_cursor.executemany(stmt, data)

    # connection is not autocommit by default. So we must commit to save our changes.
    connection.commit()

    print("done")


except Error as e:
    print(e)

finally:
    # Close the connection
    connection.close()
