import datetime
from pymongo import MongoClient

import os, re

def enum(**enums):
    return type('Enum', (), enums)

class FeedServer:
	client = MongoClient('localhost', 27017)
	db = client.MINOR
	db_feeds = db.Feeds
	db_articles = db.Articles
	
	FeedType = enum(twitter="twitter", flickr="flickr", rss="rss")
	
	ParserRegex = re.compile('([a-zA-Z0-9]+)_parser\.py$')
	FeedParsers = {}
	
	def __init__(self):
		path = os.path.dirname(os.path.abspath(__file__))
		for file in os.listdir(path):
			match = self.ParserRegex.match(file)		
			if match is not None:
				name = match.group(1)
				if name not in self.FeedParsers:
					self.FeedParsers[name] = None
		for name in self.FeedParsers:
			self.FeedParsers[name] = __import__(name + "_parser", globals())
	
	def _invoke_parser(self, parser, url):
		return getattr(self.FeedParsers[parser], "parse")(url)
		
	
	def _type(self, url):
		if (url.find('twitter.com') != -1):
			return self.FeedType.twitter
		elif (url.find('flickr.com') != -1):
			return self.FeedType.flickr
		else:
			return self.FeedType.rss
		
	def append(self, url):
		feed = self.db_feeds.find_one({'url': url})
		if feed is None:
			id = self.db_feeds.insert({
				'url': url,
			})
			feed = self._update(id, url)
			self.db_feeds.update({'_id': id}, {'$set': {
				'title': feed['title'],
				'subtitle': feed['subtitle'],
				'link': feed['link'],
				'last_update': datetime.datetime.now()
			}})
			return id
		return feed['_id']
	
	def _update(self, id, url):
		feed = self._invoke_parser(self._type(url), url)
		update_count = 0
		for article in feed['articles']:
			if self.db_articles.find_one({'feed': id, 'link': article['link'], 'date': article['date']}) is None:
				self.db_articles.insert({
					'feed': id,
					'title': article['title'],
					'content': article['content'],
					'author': article['author'],
					'link': article['link'],
					'date': article['date'],
					'readed': 0,
					'stared': 0,
				})
				update_count = update_count + 1
		feed['update_count'] = update_count
		return feed
		
	def update(self):
		feeds = self.db_feeds.find(fields=['url'])
		for feed in feeds:
			update_count = self._update(feed['_id'], feed['url'])['update_count']
			print '%4d updated in %s' % (update_count, feed['url'])
