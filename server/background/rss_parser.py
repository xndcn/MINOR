import urllib2
import feedparser
import datetime, time

import lxml.html

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
		html = lxml.html.fromstring(entry.summary)
		img = html.xpath("//img")
		text = html.text_content().strip()
		if img is not None and len(img) > 0:
			img = img[0].attrib['src']
		else:
			img = ''
	
		article = {
			'title': entry.title,
			'content': text,
			'author': entry.author if 'author' in entry else '',
			'link': entry.link,
			'photo': img,
			'date': datetime.datetime.fromtimestamp(time.mktime(entry.updated_parsed))
		}
		feed['articles'].append(article)
	return feed
