from pymongo import MongoClient
from bson.objectid import ObjectId
from background.FeedServer import FeedServer

class User:
	client = MongoClient('10.101.158.66', 27017)
	db = client.MINOR
	db_user_feeds = db.UserFeeds
	db_users = db.Users
	db_feeds = db.Feeds
	db_articles = db.Articles
	
	feedServer = FeedServer()
	
	def verify(self, username, password):
		user = self.db_users.find_one({'name': username, 'password': password})
		if user is None:
			return False
		else:
			return True
			
	def append(self, username, url):
		feedid = self.feedServer.append(url)
		userid = self.db_users.find_one({'name': username})['_id']
		if self.db_user_feeds.find_one({'userid': userid, 'feedid': feedid}) is None:			
			self.db_user_feeds.insert({'userid': userid, 'feedid': feedid})
			
	def feeds(self, username):
		userid = self.db_users.find_one({'name': username})['_id']
		user_feeds = self.db_user_feeds.find({'userid': userid})
		feeds = []
		for feed in user_feeds:
			feedid = feed['feedid']
			db_feed = self.db_feeds.find_one({'_id': feedid})
			feeds.append({
				'id': str(db_feed['_id']),
				'title': db_feed['title'],
			})
		return feeds
		
	def articles(self, username, feedid):
		feedid = ObjectId(feedid)
		userid = self.db_users.find_one({'name': username})['_id']
		db_articles = self.db_articles.find({'feed': feedid})
		articles = {}
		
		for article in db_articles:
			article_id = article['_id']
			articles.append({
				'id': article_id,
			})		
