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
			db.close()
		except:
			articles = [news.Article("error", "error", "error", "error", "error")]

		# limit the number of articles to 25
		articles = articles[:-40:-1] # TODO: sort articles by pub date
		# TODO: this *does* do fetch order .... more or less date?

		if tags == 'favicon.ico':
			tags = None
		
		out = []
		if not tags:
			out = articles
		else:
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
		title, url, body = news.viewtext(url)
		header = "<h1><a href=\"%s\">%s</a></h1>" % (url, title)
		return header+body

	@route("/diffbot", 'GET')
	def diffbot():
		url = request.GET.get('url', "ERROR, please try a different link")
		title, url, text = news.diffbot(url)
		header = "<h1><a href=\"%s\">%s</a></h1>" % (url, title)
		body = news.htmlFromText(text)
		return header+body
	
	@route("/boilerpipe/", 'GET')
	def boilerpipe():
		url = request.GET.get('url', "ERROR, please try a different link")
		title, url, text = news.boilerpipe(url)
		header = "<h1><a href=\"%s\">%s</a></h1>" % (url, title)
		body = news.htmlFromText(text)
		return header+body

application = default_app()
#from bottle import debug, run
#debug(True)
#run(host='localhost', port=8080)
