# -*- coding: utf-8 -*-

import urllib2
import feedparser
import json

data = urllib2.urlopen('http://www.engadget.com/rss.xml')
d = feedparser.parse(data.read())

date = []

for entry in d.entries:
	adate = entry.updated_parsed
	slide = {
		"headline": entry.title,
		"text": entry.summary,
		"startDate": "%d,%d,%d,%d,%d,%d" % (adate.tm_year, adate.tm_mon, adate.tm_mday, adate.tm_hour, adate.tm_min, adate.tm_sec)
	}
	date.append(slide)

timeline = {
	"headline": d.feed.title,
	"type": "default",
	"text": d.feed.subtitle,
	"date": date
}

output = {"timeline": timeline}

print json.dumps(output)
