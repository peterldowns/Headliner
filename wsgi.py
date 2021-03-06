import json # for returning information on articles
import news # get the news
from db_wrapper import getCollection # load articles
from bottle import route, request, view, static_file, default_app, debug # web framework
debug(True)

class static_files():
	# serves any static files
	@route('/static/:path#.+#')
	def serve(path):
		return static_file(path, root='./static')

class index():
	# serves the main page
	@route('/favicon.ico', 'GET')
	def favicon():
		return static_file('favicon.ico', root='./static')

	@route('/', 'GET')
	@route('/:tags', 'GET')
	@view('index')
	def get(tags=None):
		try:
			coll = getCollection("news", "articles")
			tags = None # skips tags
			if tags: # BROKEN - skipped for now
				print "There are tags!"
				tags = tags.lower().split(',')
				can_have = [ {"tags" : t[1:]} for t in tags if t[0] != '^' ]
				#cant_have = [ {"tags" : t[1:]} for t in tags if t[0] == '^' ]
				params = {"$or" : can_have}
				articles = coll.find(params)
			else:
				articles = coll.find()
		except:
			articles = [news.createArticle("Error", "Error", "Error", "Error", "Error")]
		return {"articles" : articles.sort("timestamp", -1).limit(50)}
	
	@route('/viewtext', 'GET')
	def viewtext():
		url = request.GET.get('url', "ERROR, please try a different link")
		try:
			DBarticles = getCollection("news", "articles")
			match = DBarticles.find_one({"url":url})
			if match:
				out = match['html']
				print "Cache-hit => %s" % url
				if not out:
					print "\tNope, refetching"
					title, _, body = news.viewtext(url)
					try:
						body = news.html_escape(body) # clean up the body?
					except Exception as e:
						print "!!! Could not HTML escape the body of text"
						print e
					out = json.dumps({"title":match['title'], "body":body, "url":url})
					match['html'] = out
					DBarticles.save(match) # can't change size on capped collection - how to fix?
				return  out
		except Exception as e:
			print >> sys.stderr, e
		
		return {"title":"Error" ,"body":"Error", "url":"Error"}

application = default_app()
