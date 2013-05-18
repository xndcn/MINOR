from pymongo import MongoClient
import random

def marker():
    n = random.random()
    if n > .9:
        m = random.random()
        if m > .6:
            return (True, True)
        else:
            return (True, False)
    else:
        return (False, False) 

client = MongoClient('10.101.158.66', 27017)
db = client.MINOR

db_users = db.Users
db_feeds = db.Feeds
db_articles = db.Articles
db_userFeeds = db.UserFeeds
db_userActivities = db.UserActivities

user_list = []

for user in db_users.find():
    user_list.append(user['_id'])

# clear up user activity
for activity in db_userActivities.find():
    db_userActivities.remove(activity)

for u in user_list:
    for article in db_articles.find():
        mark = marker()
        db_userActivities.insert({'articleid' : article['_id'],
                                  'userid' : u,
                                  'read' : mark[0],
                                  'star' : mark[1]
                                  })


# clear up user feed
for feed in db_userFeeds.find():
    db_userFeeds.remove(feed)

for u in user_list:
    for feed in db_feeds.find():
        db_userFeeds.insert({'feedid' : feed['_id'],
                             'userid' : u})

