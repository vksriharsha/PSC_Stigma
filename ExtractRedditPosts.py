from google.cloud import bigquery
import pymysql
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/harshavk/Documents/Harsha/Spring2021/RevHack/RevolutionHackathon2021-4c1dc08620c9.json"

def sanitize(value):
  if type(value) is list:
    return str(value)
  if type(value) is dict:
    return str(value)
  # this may be required for other types
  return value

def query_reddit_posts():
    try:
        # create connection
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='pscstigma',
                                     db='psc_stigma')

        subreddits = ['alcohol', 'alcoholicsanonymous', 'alcoholism', 'stopdrinking', 'dryalcoholics',
                      'REDDITORSINRECOVERY', 'Alcoholism_Medication', 'addiction', 'Sober', 'meth', 'Drugs', 'leaves',
                      'cocaine']

        tables = ['2015_12', '2016_01', '2016_02', '2016_03','2016_04','2016_05','2016_06','2016_07','2016_08','2016_09','2016_10','2016_11','2016_12',
                  '2017_01','2017_02','2017_03','2017_04','2017_05','2017_06','2017_07','2017_08','2017_09','2017_10','2017_11','2017_12',
                  '2018_01','2018_02','2018_03','2018_04','2018_05','2018_06','2018_07','2018_08','2018_09','2018_10','2018_11','2018_12',
                  '2019_01','2019_02','2019_03','2019_04','2019_05','2019_06','2019_07','2019_08']

        for subreddit in subreddits:

            for table in tables:

                # Create cursor
                my_cursor = connection.cursor()

                stmt = "INSERT INTO reddit_posts (created_utc, subreddit, author, dom, url, num_comments,  score, ups, downs, title, selftext, saved, id, from_kind, glided, from_, stickied, retrieved_on, over_18, thumbnail, subreddit_id, hide_score, link_flair_css_class, author_flair_css_class, archived, is_self, from_id, permalink, name, author_flair_text, quarantine, link_flair_text, distinguished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                client = bigquery.Client()
                query_job = client.query(
                """
                SELECT *
                FROM `fh-bigquery.reddit_posts."""+table+"""` where subreddit='"""+subreddit+"""'"""
                )

                results = query_job.result()  # Waits for job to complete.

                for row in results:

                    values = (sanitize(row[0]), sanitize(row[1]), sanitize(row[2]),sanitize(row[3]), sanitize(row[4]), sanitize(row[5]),sanitize(row[6]), sanitize(row[7]), sanitize(row[8]),sanitize(row[9]), sanitize(row[10]), sanitize(row[11]),sanitize(row[12]), sanitize(row[13]), sanitize(row[14]),sanitize(row[15]), sanitize(row[16]), sanitize(row[17]),sanitize(row[18]), sanitize(row[19]), sanitize(row[20]), sanitize(row[21]), sanitize(row[22]), sanitize(row[23]), sanitize(row[24]), sanitize(row[25]), sanitize(row[26]), sanitize(row[27]), sanitize(row[28]), sanitize(row[29]), sanitize(row[30]), sanitize(row[31]), sanitize(row[32]))
                    # print(values)
                    my_cursor.execute(stmt, values)


                # connection is not autocommit by default. So we must commit to save our changes.
                connection.commit()
                print(subreddit+" - "+table+" is done")



    except Exception as e:
        print(e)

    finally:
            # Close the connection
        connection.close()


if __name__ == "__main__":
    query_reddit_posts()