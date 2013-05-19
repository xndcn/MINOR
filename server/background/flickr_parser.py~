import flickr_api
import re
import datetime

api_key = 'a767f178c537e839cb947016febc0f62'
api_secret = '3b34561733dfe2dd'
flickr_api.set_keys(api_key, api_secret)
flickr_api.set_auth_handler('flickr_auth')

username_regex = re.compile('flickr\.com/photos/([a-zA-Z0-9]+)')

def parse(url):
	user = flickr_api.Person.findByUrl(url)
	
	feed = {
		'title': "%s's flickr" % user.username,
		'subtitle': user.description,
		'link': user.photosurl,
		'articles': []
	}
	
	photos = user.getPhotos(per_page=20)
	
	for entry in photos:
		article = {
			'title': entry.title,
			'content': entry.description,
			'author': user.username,
			'link': entry.getPageUrl(),
			'date': datetime.datetime.fromtimestamp(entry.posted)
		}
		feed['articles'].append(article)
	return feed
