#!/usr/bin/env python

import sys
import time
import signal

# Callback called when you run 'supervisorctl stop'
def sigterm_handler(signum, frame):
	sys.exit(0)

def main():
	import news
	from db_wrapper import loadCredentials, getDatabase, getCollection, addArticles
	try:
		creds = loadCredentials()
	except Exception as e:
		creds = None

	while True:
		out = []
		try:
			new_articles = []
			source_fns = [news.NYT_mostPopular, news.NYT_recent, news.NPR_news, news.HN_frontPage, news.TNY_news]
			for src in source_fns:
				try:
					new_articles.extend(src())
				except Exception as e: pass
			
			DB_articles = getCollection("news", "articles", creds).find()
			
			_urls = map(lambda x: x.url, DB_articles)
			for a in new_articles:
				if not a.url in _urls:
					DB_articles.insert(a)
		except Exception as e:
			print "Exception:", e
			sys.exit(0)
		time.sleep(300) # repeat this command ever 3 minutes

# Bind our callback to the SIGTERM signal and run the daemon
signal.signal(signal.SIGTERM, sigterm_handler)
main()
