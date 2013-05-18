import web
import urlparse
import json

from User import User

render = web.template.render('static/', cache=False)

urls = (
	'/', 'Index',
	'/login', 'UserLogin',
	'/([0-9a-zA-Z]+)/', 'UserIndex',
	'/([0-9a-zA-Z]+)/append', 'UserAppendFeed',
	'/([0-9a-zA-Z]+)/feeds.json', 'UserFeeds',
	'/([0-9a-zA-Z]+)/([0-9a-zA-Z]+)/articles.json', 'FeedArticles',
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


class FeedArticles:
	def GET(self, username, feedid):
		articles = self.user.articles(username, feedid)
	
if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()
