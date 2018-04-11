
import  praw
import time
import datetime
import json
import pymysql
import json
import codecs
import os
# import importlib,sys
# importlib.reload(sys)
# reload(sys)
# sys.setdefaultencoding('utf8')

# os.chdir('/home/ubuntu/Reddit')

reddit = praw.Reddit( client_id = '*',
                      client_secret ='*',
                      username= '*',
                      password= '*',
                      user_agent= '*')

# mysql_conn = pymysql.connect(host="*",
#                                user="*",
#                                password="*",
#                                db="*",
#                                port=3306,
#                                use_unicode=True,
#                                charset="utf8")
#
# cursor = mysql_conn.cursor()

reddit.config.log_requests = 1
reddit.config.store_json_result = True


data = {}
# Set 7Dayago
SevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=7))
timeStamp7Dago = int(time.mktime(SevenDayAgo.timetuple()))


def crawl( subreddit_name ):

  subreddit = reddit.subreddit(subreddit_name)
  filename = subreddit_name + 'hasReply_file.json'

  with open( filename, 'a') as f:

    for submission in subreddit.top( 'week' ):

      # 1521561600 1522425600 21-31
      # open limit of comments
      submission.comments.replace_more(limit=0)
      # change UNIX-Time to readableTime
      timeArray = time.localtime(submission.created)
      readabletime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

      #put poster data in dic
      data['author'] = str(submission.author)
      data['created_at'] = str(readabletime)
      data['title'] = str( submission.title )
      data['type'] = "Post"
      data['ReplyToWho'] = ''
      data['text'] = submission.selftext

      # sqldata = "INSERT INTO reddit_data (title, author, created_at, text, type, ReplyToWho )  VALUES (%s,%s,%s,%s,%s,%s)"
      # cursor.execute(sqldata, (
      #   str(submission.title), str(submission.author), str(readabletime), str(submission.selftext), "Post", '' ))

      json.dump(data, f )
      f.write( '\n' )

      Comments = []
      #take 1 by 1 comment data in comments
      for comment in submission.comments:

        commentdata = {}
        commentdata['author'] = str(comment.author)

        # change UNIX-Time to readableTime
        timeArray = time.localtime(comment.created)
        readabletime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        commentdata['created_at'] =  str(readabletime)
        commentdata['title'] = str( submission.title )
        commentdata['type'] = "Reply"
        # to get comment parent name
        replytowho = reddit.submission(id=comment.parent_id[3:])
        commentdata['ReplyToWho'] = str( replytowho.author )
        commentdata['text'] =  comment.body

        json.dump(commentdata, f)
        f.write('\n')
        # put in to data base
        # sqldata = "INSERT INTO reddit_data (title, author, created_at, text, type, ReplyToWho )  VALUES (%s,%s,%s,%s,%s,%s)"
        # cursor.execute(sqldata, (
        #   str(submission.title), str(submission.author), str(readabletime), str(submission.selftext), "Reply", str( replytowho.author ) ))



  f.close()
  # mysql_conn.commit()
  # cursor.close()
  # mysql_conn.close()


# Thread--------------------------------------

import threading

# crawl_thread1 = threading.Thread( target= crawl, args=('Futurology_file',))
# crawl_thread2 = threading.Thread( target= crawl, args=('hardware_file',))
# crawl_thread3 = threading.Thread( target= crawl, args=('tech_file',))
# crawl_thread4 = threading.Thread( target= crawl, args=('technology_file',))
# crawl_thread5 = threading.Thread( target= crawl, args=('EthereumClassic',))
# crawl_thread1.start()
# crawl_thread2.start()
# crawl_thread3.start()
# crawl_thread4.start()
# crawl_thread5.start()

crawl('technology')

