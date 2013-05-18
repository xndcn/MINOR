from pymongo import MongoClient
from math import sqrt

class Recommend(object):


    def __init__(self):
        super(Recommend, self).__init__()

        client = MongoClient('10.101.158.66', 27017)
        db = client.MINOR

        self.db_users = db.Users
        self.db_feeds = db.Feeds
        self.db_articles = db.Articles
        self.db_userFeeds = db.UserFeeds
        self.db_userActivities = db.UserActivities

        # user_rate[user][feed] = a value of rate
        self.user_feed_rate = {}
        self.init_rate()

        self.db_recommends = db.Recommends
        for user in self.db_users.find():
            recommend_list = self.recommend(user['name'])
            for rate, item in recommend_list:
                #print user['name'], rate, self.get_title(item)
                if rate > 0:
                    self.db_recommends.insert({'userid' : user['_id'],
                                               'feedid' : item})

#        print '-----'
#        for user in self.db_users.find():
#            for k, v in self.user_feed_rate[user['_id']].iteritems():
#                print user['name'], self.get_title(k), v

    def get_title(self, feedid):
        return self.db_feeds.find_one({'_id' : feedid})['title']

    def init_rate(self):
        for user in self.db_users.find():
            #self.user_article_rate[user['_id']] = {}

            userid = user['_id']
            self.user_feed_rate[userid] = {}

            feed_read = {}
            feed_star = {}
            for feed in self.db_userFeeds.find({'userid' : userid}):
                # feed_read[feed_id] = value of total read
                feed_read[feed['feedid']] = 0
                feed_star[feed['feedid']] = 0
                self.user_feed_rate[user['_id']][feed['feedid']] = 0

            for article in self.db_userActivities.find({'userid' : userid}):
                read = article['read']
                star = article['star']
                feed_id = self._get_feedid_by_article_id(article['articleid'])
                if read:
                    feed_read[feed_id] += 1
                if star:
                    feed_star[feed_id] += 1
            
            for feed in self.db_userFeeds.find({'userid' : userid}):
                feedid = feed['feedid']
                if feed_read[feedid] != 0:
                    self.user_feed_rate[userid][feedid] = \
                        1.0 * feed_star[feedid] / feed_read[feedid]
                else:
                    self.user_feed_rate[userid][feedid] = 0.0


    def similar(self, u1, u2):
        similarity = {}
        for k, v in self.user_feed_rate[u1].iteritems():
            if k in self.user_feed_rate[u2]:
                similarity[k] = 1

        n = len(similarity)
        if n == 0: return 0

        sum1 = sum([self.user_feed_rate[u1][item] for item in similarity])
        sum2 = sum([self.user_feed_rate[u2][item] for item in similarity])

        sum1Sq = sum([pow(self.user_feed_rate[u1][item],2) for item in \
                            similarity])
        sum2Sq = sum([pow(self.user_feed_rate[u2][item],2) for item in \
                            similarity])

        pSum = sum([self.user_feed_rate[u1][item]*self.user_feed_rate[u2][item] \
                    for item in similarity])

        num = pSum - (sum1 * sum2 / n)
        den = sqrt((sum1Sq - pow(sum1, 2)/n) * 
                   (sum2Sq - pow(sum2, 2)/n))
        if den == 0: return 0

        return num / den

    def _recommend(self, userid):
        totals = {}
        simSums = {}
        for other in self.user_feed_rate:
            if other == userid:
                continue
            sim = self.similar(userid, other)
            #print sim, userid, other
            
            if sim <= 0:
                continue


            for item in self.user_feed_rate[other]:
                if item not in self.user_feed_rate[userid] or \
                        self.user_feed_rate[userid][item] == 0:
                    totals.setdefault(item, 0)
                    totals[item] += self.user_feed_rate[other][item] * \
                                    sim
                    simSums.setdefault(item, 0)
                    simSums[item] += sim

        rankings = [(total / simSums[item], item) for item, total in \
                        totals.items()]
        rankings.sort()
        rankings.reverse()
        return rankings

    def recommend(self, username):
        _id = self.db_users.find_one({'name' : username})['_id']
        return self._recommend(_id)

        
    def _get_feedid_by_article_id(self, article_id):
        return self.db_articles.find_one({'_id' : article_id})['feed']



if __name__ == '__main__':
    recommend = Recommend()
    print recommend.recommend('can')
