from pymongo import MongoClient
from bson.objectid import ObjectId
from background.FeedServer import FeedServer

import lxml.html

import datetime
import random

from urlparse import urlparse

def enum(**enums):
	return type('Enum', (), enums)

class User:
	client = MongoClient('localhost', 27017)
	db = client.MINOR
	db_user_feeds = db.UserFeeds
	db_users = db.Users
	db_feeds = db.Feeds
	db_articles = db.Articles
	db_user_activities = db.UserActivities
	
	feedServer = FeedServer()
	
	FeedType = enum(twitter="twitter", flickr="flickr", rss="rss")
	
	def _type(self, url):
		if (url.find('twitter.com') != -1):
			return self.FeedType.twitter
		elif (url.find('flickr.com') != -1):
			return self.FeedType.flickr
		else:
			return self.FeedType.rss
	
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
			url = urlparse(db_feed['link'])
			feeds.append({
				'id': str(db_feed['_id']),
				'title': db_feed['title'],
				"icon": "%s://%s/favicon.ico" % (url.scheme, url.netloc), 
			})
		return feeds
		
	def article(self, username, articleid):
		userid = self.db_users.find_one({'name': username})['_id']
		article = self.db_articles.find_one({'_id': articleid})
		article_id = article['_id']
		url = urlparse(article['link'])
		if 'photo' in article:
			img = article['photo']
		else:
			img = ''
		text = article['content']
		if img != '':
			layout = 'leftright' if random.random() > 0.4 else 'updown'
			imageUrl = img
		else:
			layout = 'onlytext'
			imageUrl = ""
			
		active = self.db_user_activities.find_one({'userid': userid, 'articleid': article_id})
		
		type = self._type(article['link'])
				
		icon = '/static/images/%s_icon.png' % type
		if active is not None:
			if 'star' in active and active['star']:
				icon = '/static/images/%s_icon_light.png' % type
			elif 'read' in active and active['read']:
				icon = '/static/images/%s_icon_grey.png' % type
		
			
		return {
			'layout': layout,				
			'time': article['date'],
			'text': text,
			"targetUrl": article['link'],
			'imageUrl': imageUrl,
			"iconUrl": icon,
			#"iconUrl": "%s://%s/favicon.ico" % (url.scheme, url.netloc), #"/static/images/eventIcon.png",
			"headline": "",
			'id': str(article_id),
		}
		
	def articles(self, username, feedid):
		feedid = ObjectId(feedid)
		userid = self.db_users.find_one({'name': username})['_id']
		db_articles = self.db_articles.find({'feed': feedid})
		myarticles = []
		
		
		for article in db_articles:
			article_id = article['_id']
			url = urlparse(article['link'])
			if 'photo' in article:
				img = article['photo']
			else:
				img = ''
			text = article['content']
			if img != '':
				layout = 'leftright' if random.random() > 0.4 else 'updown'
				imageUrl = img
			else:
				layout = 'onlytext'
				imageUrl = ""
				
			active = self.db_user_activities.find_one({'userid': userid, 'articleid': article_id})
			
			type = self._type(article['link'])
					
			icon = '/static/images/%s_icon.png' % type
			if active is not None:
				if 'star' in active and active['star']:
					icon = '/static/images/%s_icon_light.png' % type
				elif 'read' in active and active['read']:
					icon = '/static/images/%s_icon_grey.png' % type
			
				
			myarticles.append({
				'layout': layout,				
				'time': article['date'],
				'text': text,
				"targetUrl": article['link'],
				'imageUrl': imageUrl,
				"iconUrl": icon,
				#"iconUrl": "%s://%s/favicon.ico" % (url.scheme, url.netloc), #"/static/images/eventIcon.png",
				"headline": "",
				'id': str(article_id),
			})
		
		return myarticles
		
	def activity(self, username, articleid, status):
		articleid = ObjectId(articleid)
		userid = self.db_users.find_one({'name': username})['_id']
		#article = self.db_articles.find_one({'_id': articleid})
		#feedid = article['feed']
		self.db_user_activities.update({'userid': userid, 'articleid': articleid}, {'$set': {
			status: True,
		}}, upsert=True)
		self.db_articles.update({'_id': articleid}, {'$inc': {
			('%sed' % status): 1,
		}})
		return
