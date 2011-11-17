#!/usr/bin/env python

import sys
import time
import signal

# Callback called when you run `supervisorctl stop'
def sigterm_handler(signum, frame):
    print >> sys.stderr, "Kaboom Baby!"
	sys.exit(0)

def main():
	while True:
		print >> sys.stderr, "Tick"
		time.sleep(1)

# Bind our callback to the SIGTERM signal and run the daemon:
signal.signal(signal.SIGTERM, sigterm_handler)
main()

"""
#!/usr/bin/env python
import sys
import time
import signal
import shelve
import news
# SIGINT handler

def sigterm_handler(signum, frame):
	cur_time = time.asctime(time.localtime(time.time()))
	print >> sys.stderr, "Interrupted at %s" % cur_time
	sys.exit(0)


def main():
	#cur_time = time.asctime(time.localtime(time.time()))
	#print >> sys.stderr, "Program was run at %s" % cur_time
	
	new_articles = news.AP_topNews(20)
	new_articles.extend(news.NYT_mostPopular())

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
			added += 1
			out.append(a)
	db['articles']	= out

	
	cur_time = time.asctime(time.localtime(time.time()))
	print >> sys.stderr, "@ %s: num_articles=%d, new=%d" % (cur_time, len(out), added)
	db.close()
	return

def do():
	while True:
		print "== RUNNING MAIN =="
		main()
		print "== FINISHED MAIN =="
		time.sleep(60)


# Bind our handler to SIGINT
signal.signal(signal.SIGTERM, sigterm_handler)
# Run the main program
do()
"""
