import news # get the news
from bottle import debug, run, template, route, request, view, static_file, default_app # run a web app

debug(True)

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
		if tags == 'favicon.ico':
			tags = None
		articles = news.NYT_mostPopular()
		articles.extend(news.AP_topNews())
		out = []
		if not tags:
			out = articles
		else:
			print "filtering tags"
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
	
	@route('/viewtext/:url#.+#', 'GET')
	def viewtext(url):
		title, url, body = news.viewtext(url)
		header = "<h1><a href=\"%s\">%s</a></h1>" % (url, title)
		return header+body

	@route("/diffbot/:url#.+#", 'GET')
	def diffbot(url):
		title, url, text = news.diffbot(url)
		header = "<h1><a href=\"%s\">%s</a></h1>" % (url, title)
		body = news.htmlFromText(text)
		return header+body
	
	@route("/boilerpipe/:url#.+#", 'GET')
	def boilerpipe(url):
		title, url, text = news.boilerpipe(url)
		header = "<h1><a href=\"%s\">%s</a></h1>" % (url, title)
		body = news.htmlFromText(text)
		return header+body

application = default_app()
run(host='localhost', port=8080)
