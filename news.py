import requests # fetch articles
import urllib # escape requests
import json # parse result
import BeautifulSoup, re # html cleaning
import time # delay AP requests, make timestamps

# debugging
import sys, traceback

def html_escape(s):
	out = s
	try:
		out = s.decode('utf-8').encode('ascii', 'xmlcharrefreplace')
	except Exception as e:
		print "html_escape error:",s,e
		exc_type, exc_value, exc_traceback = sys.exc_info()
		print "*** print_tb:"
		traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
		print "*** print_exception:"
		traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)
		print "*** print_exc:"
		traceback.print_exc()
	return unicode(out)

def cleanText(text):
	""" Cleans text """
	out = re.sub(r'[\t]+', '&nbsp;'*4, text)
	out = re.sub(r'[\r\n]+', '\n', out)
	return out

def htmlFromText(text):
	""" Given a plain text input, clean it up and try to turn it into HTML """
	html = cleanText(text)
	'</p><br><p>'.join(html.split('\n'))
	html = "<p>%s</p>" % html
	return html
	
def boilerpipe(url):
	format = "json"
	extractor_address = "http://boilerpipe-web.appspot.com/extract?url=%s&output=%s&mode=default" % (urllib.quote(url), format)
	
	resp = requests.get(extractor_address)
	data = json.loads(resp.content)["response"]
	
	#print json.dumps(data, sort_keys=True, indent=4)
	url = data["source"]
	text = data["content"]
	title = data["title"] # this is the page title, not the article title
	return (title, url, text)
	
def diffbot(url):
	""" use the diffbot.com api to extract article text """
	token = "b674b393db9437307b5f9807ddbc7d27"
	format = "json" # by default, but specified for readability
	extractor_address = "http://www.diffbot.com/api/article?token=%s&url=%s&format=%s" % (token, urllib.quote(url), format)
	
	resp = requests.get(extractor_address)
	data = json.loads(resp.content)
	
	#print json.dumps(data.keys(), sort_keys=True, indent=4)
	url = data.get("url", None)
	text = data.get("text", None)
	title = data.get("title", None)
	return (title, url, text)

def viewtext(url):
	""" Use viewtext.org's API to extract the HTML from an article """
	viewtext = "http://viewtext.org/api/text?url=%s&format=%s&rl=%s"
	redirect_links = "false"
	form = "json"
	req_string = viewtext % (urllib.quote(url), form, redirect_links)
	resp = requests.get(req_string)
	data = json.loads(resp.content)
	
	content = data.get("content", "")
	title = data.get("title", "")
	return (title, url, content)
	
def createArticle(url, source, pub_date, tags, title=None):
	try:
		return {
		"source" : html_escape(source),
		"url" : url,
		"pub_date" : pub_date,
		"timestamp" : time.time()*1000, # timestamp in ms since epoch, for JS compatibility
		"tags" : map(unicode.lower, map(html_escape, tags)), # lower case them
		"title" : html_escape(title),
		"html" : None,
		"value" : 0 }
	except Exception as e:
		print "Error in article creation:"
		print "\t",e

NYT_keys = {
	"most-popular" : "32a8ad498501475cb0fa4abbc04f4e4e:5:61481359",
	"article-search" : "6e9f5b717ddf385cb182ae1a2c24b28c:6:61481359",
	"times-tags" : "0c826cfa738585b372f283434b5f1a91:18:61481359",
	"news-wire" : "f005f0ec03d16bf552cd581e15ce9348:7:61481359",
	"people" : "102d67e1500d8780ff52c6c8171375d4:8:61481359"
}
AP_keys = {
	"breaking-news" : "jdtcpmm95unxu84vwuvhnuav"
}
NPR_key = "MDA4NDY3NzI0MDEzMjEwNjExOTdkMDUyMA001"

def APcats():
	""" Get all of the different categories of AP news, with keys """
	APkey = AP_keys["breaking-news"]
	base = "Http://developerapi.ap.org/v2/categories.svc/?apiKey=%s"
	r = requests.get(base % APkey)
	soup = BeautifulSoup.BeautifulSoup(r.content, convertEntities=['xml', 'html'])
	for entry in soup.findAll('entry'):
		name = str(entry.title.string)
		id = str(entry.id.string).split(':')[-1]
		yield "%s,%s" % (id, name)


def NPR_get_articles(jresp):
	""" Given an NPR json structure, return a list of articles """
	stories = jresp['list']['story']
	num = len(stories)
	
	articles = []
	for story in stories:
		pub_date = story['pubDate']['$text']
		title = story['title']['$text']
		source = "NPR"
		url = story['link'][0]['$text']
		url = url.split("?")[0] # remove any get params
		
		# there aren't really any tags... doing my best
		tags = []
		tags.append(story['slug']['$text'])
		tags.extend(story['teaser']['$text'].split(' '))
		
		# make the article
		a = createArticle(url, source, pub_date, tags, title)
		
		articles.append(a)
	
	return articles

def NPR_news():
	""" Fetch all NPR news """
	id = 1001 # "News"
	fields = "summary" #",".join(["summary"])
	required_assets = "text" #",".join(["text"])
	count = 10
	base = "http://api.npr.org/query?id=%d&fields=%s&requiredAssets=%s&dateType=story&sort=dateDesc&output=JSON&numResults=%d&apiKey=%s"
	reqstr = base % (id, fields, required_assets, count, NPR_key)
	r = requests.get(reqstr)
	jresp = json.loads(r.content)
	return NPR_get_articles(jresp)


def AP_topNews():
	""" Fetches all AP news in given categories """
	categories = [
		#31990, # Top General Short Headlines
		#31991, # Top International Short Headlines
		#31992, # Top Technology Short Headlines
		#31993, # Top Sports Short Headlines
		#31994, # Top Business Short Headlines
		#31995, # General Financial/Business News
		#31998, # National News
		#32005, # High Tech News
		#32502, # Europe News
		#32503, # Africa News
		#32505, # Middle East News
		#32506, # Feature Stories
		#32516, # President, White House, Advisers News
		#32518, # Congress News
		#32519, # Supreme Court news
		#32520, # Other U.S. Government News
		#32526, # Personal Finance, Investing and Consumer News
		#32530, # Wall Street Stock reports
		#32539, # Science News
		#32573, # Top Political Short Headlines
		41664, # Top News
	]
	articles = []
	for c in categories:
		try:
			#time.sleep(3) # rate limiting protection
			articles.extend(AP_news(c))
		except Exception as e:
			print "Failed to fetch AP %d" % c
			print "Traceback:", e
	return articles

def TNY_news():
	base = "http://www.newyorker.com/services/mrss/feeds/everything.xml"
	r = requests.get(base)
	soup = BeautifulSoup.BeautifulStoneSoup(r.content, convertEntities=['xml', 'html'])
	
	articles = []
	for item in soup.findAll('item'):
		url = str(item.link.string).split("?")[0]
		title = item.title.string
		source = "The New Yorker"
		pub_date = item.pubdate.string
		tags = str(item.description.string).split('&#160;.')[0].split(' ')
		a = createArticle(url, source, pub_date, tags, title)
		articles.append(a)
	return articles
		
def AP_news(category):
	""" Gets AP news on a category """
	count = 5
	APkey = AP_keys["breaking-news"]
	#category = 41664 # AP Online Top General Short Headlines
	contentOption = 1
	base = "http://developerapi.ap.org/v2/categories.svc/%d/?contentOption=%d&count=%d"\
		"&mediaOption=0&apiKey=%s"
	reqstr = base % (category, contentOption, count, APkey)
	r = requests.get(reqstr)
	soup = BeautifulSoup.BeautifulSoup(r.content, convertEntities=['xml','html'])

	articles = []
	for entry in soup.findAll('entry'):
		url = str(entry.link["href"])
		url = url.split("?")[0] # remove any get params
		title = str(entry.title.string)
		source = "Associated Press"
		pub_date = str(entry.updated.string.split('T')[0])
		
		tags = []
		tags.extend([str(cat['label']) for cat in entry.findAll('category')])
		a = createArticle(url, source, pub_date, tags, title)
		if contentOption == 2: # if we get the source text with it, may as well use it
			entry_content = entry.findAll(attrs={"class":"entry-content"})[0].contents
			a.html = "".join(map(str, entry_content))
			a.text = " ".join(map(lambda x: re.sub(r'<[^>]+>', '', str(x)), entry_content))
		articles.append(a)
	return articles


def NYT_get_articles(jresp):
	""" Given a json response formatted according to NYT's
		guidelines, return a list of articles """
	articles = []
	for data in jresp["results"]:
		url = data["url"]
		url = url.split("?")[0] # remove any get params
		title = data["title"]
		source = data["source"]
		pub_date = data["published_date"]
		
		# tags
		tags = []
		tags.extend(title.split(' '))
		tags.append(data.get("section", ""))

		for tt in ["org_facet", "geo_facet", "des_facet"]:
			# organizations, newspaper section, geography, NYT tags
			try:
				tags.extend(data.get(tt, [])) # organizations
			except TypeError as te:
				pass
		
		try:
			for perstr in data.get("per_facet", []): # people
				fl = perstr.split(", ")
				if len(fl) == 2:
					last, first = perstr.split(", ")
					first = first.split()[0]
					tags.append(" ".join([first, last]))
				else:
					tags.append(perstr)
		except TypeError as te:
			pass
		
		a = createArticle(url, source, pub_date, tags, title)
		articles.append(a)
	return articles

def NYT_recent(num_days=1, source="all", sec_list=["all"]):
	""" Get the most recent NYT news """
	fmt = "json"
	sections = ";".join(sec_list)
	key = NYT_keys["news-wire"]
	base = "http://api.nytimes.com/svc/news/v3/content/%s/%s/%d.%s?api-key=%s"
	req_str = base % (source, sections, num_days, fmt, key)
	r = requests.get(req_str)
	jresp = json.loads(r.content)
	return NYT_get_articles(jresp)

def NYT_mostPopular(num_days=1, type="mostviewed", sec_list=["all-sections"]):
	""" Get the most popular NYT news"""
	#type = "mostemailed" / type = "mostshared"
	sections = ";".join(sec_list)
	base = "http://api.nytimes.com/svc/mostpopular/v2/%s/%s/%d.json"\
		"?api-key=32a8ad498501475cb0fa4abbc04f4e4e:5:61481359"
	r = requests.get(base % (type, sections, num_days))
	jresp = json.loads(r.content)
	
	return NYT_get_articles(jresp)

def HN_frontPage():
	""" Return the links on news.ycombinator.com's front page """
	base = "http://api.ihackernews.com/page"
	r = requests.get(base)
	jresp = json.loads(r.content)
	articles = [] # url, source, pub_date, tags, title
	source = "Hacker News"
	for link in jresp['items']:
		try:
			url = link['url']
			title = link['title']
			pub_date = link['postedAgo']
			tags = title.split(' ') # lack of tags :(
			a = createArticle(url, source, pub_date, tags, title)
			articles.append(a)
		except: pass
	return articles
