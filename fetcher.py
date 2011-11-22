#!/usr/bin/env python

import time
import sys
import shelve
import news

new_articles = []
source_fns = [news.AP_topNews, news.NYT_mostPopular, news.NYT_recent, news.NPR_news, news.HN_frontPage]

for src in source_fns:
	try:
		new_articles.extend(src())
	except Exception as e:
		print "Failed to add new articles"
		print ">>", e

out = []
try:
	db = shelve.open("news.shelf")
	if not db.has_key('articles'):
		db['articles'] = []
	out = db['articles']
except:
	if db:
		db.close()
	print >> sys.stderr, "COULD NOT LOAD DATABASE news.shelf"
	sys.exit(0)

# assumed that db is real
added = 0
_urls = map(lambda x: x.url, out)
for a in new_articles:
	if not a.url in _urls:
		out.append(a)
		added += 1
db['articles']	= out
	
cur_time = time.asctime(time.localtime(time.time()))
print >> sys.stderr, "@ %s: fetched articles=%d, new articles=%d" % (cur_time, len(out), added)
db.close()
sys.exit(0)
