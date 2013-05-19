import web
import urlparse
import json
import datetime

from bson.objectid import ObjectId

from User import User

import random

from background.recommend import Recommend

render = web.template.render('static/', cache=False)

urls = (
	'/', 'Index',
	'/login', 'UserLogin',
	'/([0-9a-zA-Z]+)/', 'UserIndex',
	'/([0-9a-zA-Z]+)/append', 'UserAppendFeed',
	'/([0-9a-zA-Z]+)/feeds.json', 'UserFeeds',
	'/([0-9a-zA-Z]+)/([0-9a-zA-Z]+)/articles.json', 'FeedArticles',
	'/([0-9a-zA-Z]+)/articles.json', 'UserArticles',
	'/([0-9a-zA-Z]+)/activity', 'UserActivity',
	'/([0-9a-zA-Z]+)/([0-9a-zA-Z]+)/recommend', 'ArticleRecommend',
)

class Index:
	def GET(self):
		raise web.seeother("/static/login.html")

class UserLogin:
	user = User()
	def POST(self):
		params = web.input()
		if self.user.verify(params.username, params.password):
			raise web.seeother("/%s/" % params.username)
		else:
			raise web.seeother("/index.html")
		

class UserIndex:
	def GET(self, username):
		return render.main(username)

class UserAppendFeed:
	user = User()
	def GET(self, username):
		params = web.input()
		url = params.url
		self.user.append(username, url)
		return
		

class UserFeeds:
	user = User()
	def GET(self, username):
		feeds = self.user.feeds(username)
		return json.dumps(feeds)
		
class UserActivity:
	user = User()
	def GET(self, username):
		params = web.input()
		articleid = params.articleid
		status = params.status
		self.user.activity(username, articleid, status)
		return params


class FeedArticles:
	user = User()
	def GET(self, username, feedid):
		articles = self.user.articles(username, feedid)
		articles.sort(key=lambda article: article['time'], reverse=True)
		
		count = 0
		for article in articles:
			article['time'] = "%d,%d,%d,%d,%d,%d" % (article['time'].year, article['time'].month, article['time'].day, article['time'].hour, article['time'].minute, article['time'].second)	
			article['direction'] = 'up' if count%2==0 else 'down'
			count = count + 1		
		return json.dumps(articles)
		
class UserArticles:
	user = User()
	def GET(self, username):
		feeds = self.user.feeds(username)
		articles = []
		for feed in feeds:
			feedid = feed['id']
			articles = articles + self.user.articles(username, feedid)
		articles.sort(key=lambda article: article['time'], reverse=True)
		count = 0
		for article in articles:
			article['time'] = "%d,%d,%d,%d,%d,%d" % (article['time'].year, article['time'].month, article['time'].day, article['time'].hour, article['time'].minute, article['time'].second)	
			article['direction'] = 'up' if count%2==0 else 'down'
			count = count + 1
		return json.dumps(articles)
		
class ArticleRecommend:
	user = User()
	rec = Recommend()
	def GET(self, username, articleid):
		articleid = ObjectId(articleid)
		articles = self.rec._recommend_for_article(articleid)
		if articles is not None and len(articles)>0:
			articleid = random.choice(articles)
			article = self.user.article(username, articleid)
			article['time'] = "%d,%d,%d,%d,%d,%d" % (article['time'].year, article['time'].month, article['time'].day, article['time'].hour, article['time'].minute, article['time'].second)	
			return json.dumps(article)
		return ""
	
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
