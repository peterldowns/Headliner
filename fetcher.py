import sys
import time
import signal
import shelve
import news
"""
# SIGINT handler
def sigterm_handler(signum, frame):
	cur_time = time.asctime(time.localtime(time.time()))
	print >> sys.stderr, "Interrupted at %s" % cur_time
	sys.exit(0)


# Bind our handler to SIGINT
signal.signal(signal.SIGTERM, sigterm_handler)
"""
def main():
	#cur_time = time.asctime(time.localtime(time.time()))
	#print >> sys.stderr, "Program was run at %s" % cur_time
	
	new_articles = news.AP_topNews()
	new_articles.extend(news.NYT_mostPopular())
	new_articles.extend(news.NYT_recent())
	new_articles.extend(news.NPR_news())
	
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
		return

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

# Run the main program
main()
