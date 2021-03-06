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
			source_fns = [news.NYT_mostPopular, news.NPR_news,
						  news.HN_frontPage, news.TNY_news,
						  news.AP_topNews]
			for src in source_fns:
				try:
					new_articles.extend(src())
				except Exception as e:
					print "Error with source",src
					print "\t", e
			
			coll = getCollection("news", "articles", creds)
			print "number of old articles: %d" % coll.count()
			
			added = 0
			for a in new_articles:
				print "a.url = %s" % a['url']
				x = coll.find_one({"url":a['url']})
				if x:
					print "\t already exists: %d" % x['timestamp']
				if not x:
					print "\t Added to DB"
					coll.insert(a)
					added += 1
			print "Added %d new articles" % added
		except Exception as e:
			print "Failed to save to database, see stderr logs"
			print >> sys.stderr, "Exception:", e
		time.sleep(120) # repeat this command ever 3 minutes

# Bind our callback to the SIGTERM signal and run the daemon
signal.signal(signal.SIGTERM, sigterm_handler)
main()

