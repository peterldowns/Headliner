#!/usr/bin/env python

import time
import sys
import shelve
import news

print sys.argv
if len(sys.argv) == 2:
	location = sys.argv[1]
else:
	print >> sys.stderr, "Did not receive file argument"
	print >> sys.stderr, "Assuming /home/dotcloud/current/news.shelf is the path"
	location = "/home/dotcloud/current/news.shelf"

out = []
try:
	db = shelve.open(location)
	if not db.has_key('articles'):
		db['articles'] = []
	out = db['articles']
except Exception as e:
	print "Exception:", e
	print >> sys.stderr, "COULD NOT LOAD DATABASE news.shelf"
	sys.exit(0)

# assumed that db is real
new_articles = []
source_fns = [news.AP_topNews, news.NYT_mostPopular, news.NYT_recent, news.NPR_news, news.HN_frontPage]

for src in source_fns:
	try:
		new_articles.extend(src())
	except Exception as e:
		print "Failed to add new articles"
		print ">>", e

added = 0
_urls = map(lambda x: x.url, out)
for a in new_articles:
	if not a.url in _urls:
		out.append(a)
		added += 1
db['articles']	= out
	
cur_time = time.asctime(time.localtime(time.time()))
#print >> sys.stderr, "@ %s: fetched articles=%d, new articles=%d" % (cur_time, len(out), added)
db.close()
sys.exit(0)
