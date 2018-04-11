#!/usr/bin/env python
# coding=utf-8
import  praw
import  csv
import time
import datetime
import json
import pandas as pd
import tzlocal
from praw.models import MoreComments
import sys
import nltk
nltk.download('stopwords')

reload(sys)
sys.setdefaultencoding('utf8')

reddit = praw.Reddit( client_id = '*',
                      client_secret ='*',
                      username= '*',
                      password= '*',
                      user_agent= '*')

reddit.config.log_requests = 1
reddit.config.store_json_result = True

#--------------------------------------------------
#Spider

def crawl( subreddit_name ):

    subreddit = reddit.subreddit( subreddit_name )
    filename = subreddit_name + '_file.json'
    data = {}

    #Get SevenDayAgo
    SevenDayAgo = (datetime.datetime.now() - datetime.timedelta(days=7))
    timeStamp7Dago = int(time.mktime(SevenDayAgo.timetuple()))

    with open(filename, 'wb+') as f:

      for submission in subreddit.submissions( timeStamp7Dago, int(time.time()) ):

        commentList = list()
        for comment in submission.comments:
             if isinstance( comment , MoreComments ):
                 continue
             commentList.append(comment.body)

        submission.comments.replace_more(limit=0)

        #change UNIX-Time to readableTime
        timeArray = time.localtime(submission.created)
        readabletime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

        data['author'] = str( submission.author )
        data['created'] = readabletime
        data['title'] = submission.title
        data['comments'] = str( commentList )
        json.dump (data, f, indent=4 )

    f.close()


# crawl( 'Futurology' )
# crawl( 'hardware' )
# crawl( 'software')
crawl( 'Bitcoin+CryptoCurrency')
#crawl( 'CryptoCurrency')
# crawl( 'CryptoMarkets')

#--------------------------------------------------
#Text Pre-processing

# emoticons_str = r"""
#     (?:
#         [:=;] # Eyes
#         [oO\-]? # Nose (optional)
#         [D\)\]\(\]/\\OpP] # Mouth
#     )"""
#
# regex_str = [
#     emoticons_str,
#     r'<[^>]+>',  # HTML tags
#     r'(?:@[\w_]+)',  # @-mentions
#     r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
#     r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
#
#     r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
#     r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
#     r'(?:[\w_]+)',  # other words
#     r'(?:\S)'  # anything else
# ]
#
# tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
# emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
#
# def tokenize(s):
#     return tokens_re.findall(s)
#
# def preprocess(s, lowercase=True):
#     tokens = tokenize(s)
#     if lowercase:
#         tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
#     return tokens
#
# df = pd.read_csv('Futurology_file.csv' , names=['author', 'created', 'title', 'comment'] , quoting=csv.QUOTE_NONE , encoding='utf8'  )
#
# punctuation = list(string.punctuation)
#
# stop = stopwords.words('english') + punctuation + ['rt', 'via', 'could'] #, u'\u2018', u'\u2019', u'\u201c' , u'\u201d', u'could' ]
#
# # print(punctuation)
#
# #--------------------------------------------------
# #Term co-occurrences
#
# from collections import defaultdict
# # remember to include the other import from the previous post
#
# com = defaultdict(lambda: defaultdict(int))
#
# count_all = Counter()
#
# authorNum = df['author'].value_counts() #count author
# print( authorNum )
#
# for dfT in df['title'] :
#   dfT = unicodedata.normalize('NFKD', dfT).encode('ascii', 'ignore')
#   terms_only = [term for term in preprocess(dfT) if term not in stop]
#   # terms_bigram = bigrams(terms_only)
#   # count_all.update(terms_bigram) #
#   # count_all.update(terms_stop)
#   for i in range(len(terms_only) - 1):
#       for j in range(i + 1, len(terms_only)):
#           w1, w2 = sorted([terms_only[i], terms_only[j]])
#           if w1 != w2:
#               com[w1][w2] += 1
#
# com_max = []
# # For each term, look for the most common co-occurrent terms
# for t1 in com:
#     t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
#     for t2, t2_count in t1_max_terms:
#         com_max.append(((t1, t2), t2_count))
# # Get the most frequent co-occurrences
# terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
# print(terms_max[:10])














