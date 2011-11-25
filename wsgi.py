import json # for returning information on articles
import news # get the news
import shelve # load articles
from bottle import route, request, view, static_file, default_app # web framework

class static_files():
	# serves any static files
	@route('/static/:path#.+#')
	def serve(path):
		return static_file(path, root='./static')

class index():
	# serves the main page
	@route('/favicon.ico', 'GET')
	def favicon():
		print 'got the request'
		return static_file('favicon.ico', root='./static')

	@route('/', 'GET')
	@route('/:tags', 'GET')
	@view('index')
	def get(tags=None):
		# load the articles from a shelf
		try:
			db = shelve.open("news.shelf")
			if not db.has_key('articles'):
				db['articles'] = []
			articles = db['articles']
		except:
			articles = [news.Article("Error", "Error", "Error", "Error", "Error")]
		else:
			db.close()


		# limit the number of articles
		articles = articles[:-50:-1] # TODO: sort articles by pub date
		# TODO: this *does* do fetch order .... more or less date?

		if not tags:
			out = articles
		else:
			out = []
			tags = filter(lambda x: len(x), tags.lower().split(','))
			for a in articles:
				tagstr = " ".join(a.tags)
				do_app = False
				for t in tags:
					tmp = t.strip()
					incl = tmp[0]!='^'
					if incl and tmp in tagstr:
						do_app = True
					if (not incl) and (tmp[1:] in tagstr):
						do_app = False
						break
				if do_app:
					out.append(a)
		return dict(articles=out)
	
	@route('/viewtext', 'GET')
	def viewtext():
		url = request.GET.get('url', "ERROR, please try a different link")
		print "@viewtext: req for %s" % url
		try:
			db = shelve.open("news.shelf")
			if not db.has_key('articles'):
				db['articles'] = []
			articles = db['articles']
		except:
			articles = []
		else:
			db.close()
		
		# try to return saved json
		for a in articles:
			if url == a.url and a.html:
				print "-> returning cached HTML"
				return a.html
	
		# otherwise, fetch it again ...
		print "-> fetching from viewtext.com ..."
		title, _url, body = news.viewtext(url)
		out = json.dumps({"title":title, "body":body, "url":url})
		# div class="headline"

		# ... and save it for next time
		try:
			db = shelve.open("news.shelf")
			tmp = None
			if not db.has_key('articles'):
				tmp = []
			else:
				tmp = db['articles']
			for a in tmp:
				if a.url == url:
					a.html = out
					print "   (cached result for later)"
					break
			db['articles'] = tmp
		except: pass
		else:
			db.close()

		return out

application = default_app()
from bottle import debug, run
debug(True)
run(host='localhost', port=8080)
