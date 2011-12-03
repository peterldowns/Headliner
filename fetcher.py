#!/usr/bin/env python

import sys
import time
import signal

# Callback called when you run 'supervisorctl stop'
def sigterm_handler(signum, frame):
	sys.exit(0)

def main():
	import shelve
	import news
	if len(sys.argv) == 2:
		location = sys.argv[1]
	else:
		location = "/home/dotcloud/current/news.shelf"
	while True:
		out = []
		try:
			db = shelve.open(location)
			if not db.has_key('articles'):
				db['articles'] = []
			out = db['articles']
			new_articles = []
			source_fns = [news.AP_topNews, news.NYT_mostPopular, news.NYT_recent, news.NPR_news, news.HN_frontPage, news.TNY_news]
			for src in source_fns:
				try:
					new_articles.extend(src())
				except Exception as e:
					pass #print "Failed to add new articles\n>>", e
			added = 0
			_urls = map(lambda x: x.url, out)
			for a in new_articles:
				if not a.url in _urls:
					out.append(a)
					added += 1
			db['articles']	= out
			db.close()
		except Exception as e:
			print "Exception:", e
			print >> sys.stderr, "COULD NOT LOAD DATABASE news.shelf"
			sys.exit(0)
		time.sleep(300) # repeat this command ever 3 minutes

# Bind our callback to the SIGTERM signal and run the daemon
signal.signal(signal.SIGTERM, sigterm_handler)
main()
