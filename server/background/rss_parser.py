import urllib2
import feedparser
import datetime, time

def parse(url):
	data = urllib2.urlopen(url)
	d = feedparser.parse(data.read())
	
	feed = {
		'title': d.feed.title,
		'subtitle': d.feed.subtitle,
		'link': d.feed.link,
		'articles': []
	}
	
	for entry in d.entries:
		article = {
			'title': entry.title,
			'content': entry.summary,
			'author': entry.author if 'author' in entry else '',
			'link': entry.link,
			'date': datetime.datetime.fromtimestamp(time.mktime(entry.updated_parsed))
		}
		feed['articles'].append(article)
	return feed
