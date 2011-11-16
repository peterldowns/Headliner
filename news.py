import requests # fetch articles
import json # parse result
import BeautifulSoup, re # html cleaning

def cleanHTML(html):
	""" Removes all custom / unuseful HTML tags from a given body of HTML """
	VALID_TAGS = ['h1', 'h2', 'h3', 'h4',
				  'h5', 'h6', 'p', 'a', 'img',
				  'b', 'em', 'div', 'span']
	soup = BeautifulSoup.BeautifulSoup(html)
	for tag in soup.findAll(True):
		if tag.name not in VALID_TAGS:
			tag.extract()
	# now delete all HTML comments (<!-- comment -->)
	comments = soup.findAll(a=lambda a:isinstance(a, BeautifulSoup.Comment))

	[comment.extract() for comment in comments] # extracts each comment
	return soup.renderContents()

def cleanText(text):
	out = re.sub(r'[\t]+', '&nbsp;'*4, text)
	out = re.sub(r'[\r\n]+', '\n', out)
	return out

def textFromHTML(html):
	""" Given some HTML input, cleans it up and tries to remove all the tags
		so that it can be treated as plain text """
	text = cleanHTML(html)
	text = re.sub(r'<[^>]+>', '', text) # get rid of all tags, but not their contents
	#text = re.sub(r'\s+', ' ', text) # change multiple whitespace in a row to a single space
	return text
	
def htmlFromText(text):
	""" Given a plain text input, clean it up and try to turn it into HTML """
	html = cleanText(text)
	'</p><br><p>'.join(html.split('\n'))
	html = "<p>%s</p>" % html
	return html

	
""" TEXT/HTML EXTRACTORS """
def boilerpipe(url):
	format = "json"
	extractor_address = "http://boilerpipe-web.appspot.com/extract?url=%s&output=%s&mode=default" % (url, format)
	
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
	extractor_address = "http://www.diffbot.com/api/article?token=%s&url=%s&format=%s" % (token, url, format)
	
	resp = requests.get(extractor_address)
	data = json.loads(resp.content)
	
	#print json.dumps(data.keys(), sort_keys=True, indent=4)
	url = data.get("url", None)
	text = data.get("text", None)
	title = data.get("title", None)
	return (title, url, text)

def viewtext(url):
	""" Use viewtext.org's API to extract the HTML from an article """
	viewtext = "http://viewtext.org/api/text?url=%s&format=%s"
	format = "json"
	req_string = viewtext % (url, format)
	
	resp = requests.get(req_string)
	data = json.loads(resp.content)
	
	#print json.dumps(data, sort_keys=True, indent=4)
	url = data["responseUrl"]
	content = data["content"]
	title = data["title"]
	print 'woopee!...'
	return (title, url, content)
	
class Article:
	def __init__(self, url, source, pub_date, tags, title=None):
		""" Set up an article structure """
		self.url = url				# string, url, "http://nytimes.com/article/baghdadexplosion"
		self.source = source		# string, source, "New York Times" 
		self.pub_date = pub_date 	# string, publication date, "11-11-11"
		self.tags = tags			# list of strings, tags, ["bomb", "baghdad", "explosion"]
		self.title = title 			# article title
		
		self.html = None			# html of article
		self.text = None			# plain text of article
		
		self.abstract = None		# 1 line description

	def getHTML(self):
		""" Return the HTMl of an article, fetching it first if necessary """
		if self.html: # if it exists, don't do anything
			pass
		elif self.text: # if we already have the plaintext, turn THAT into the HTML
			self.html = htmlFromText(self.text)
		else: # worst case scenario, make a call to the viewtext website and grab it from there
			title, url, html = viewtext(self.url)
			self.html = cleanHTML(html)
			if not self.title:
				self.title = title
		return self.html
	
	def getText(self):
		""" Return the plain text of an article, fetching it first if necessary """
		if self.text: # if it exists, don't do anything
			pass
		elif self.html: # if we already have the HTML, extract the plaintext from it
			self.text = textFromHTML(self.html)
		else: # worst case scenario, make a call ot the diffbot website and grab the plaintext
			title, url, text = diffbot(self.url)
			self.text = text
			if not self.text: # WARNING: RECURSION FOREVER????
				self.getHTML()
				self.text = self.getText()
			if not self.title:
				self.title = title
		return self.text
	
	def getAbstract(self):
		if self.abstract:
			pass
		else:
			abstract_length = 50 #number of words in the abstract
			self.abstract = " ".join(self.getText().split()[0:abstract_length])
			self.abstract = " ".join([self.abstract, "..."])
		return self.abstract

""" API KEYS """
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

def APcats():
	APkey = AP_keys["breaking-news"]
	base = "Http://developerapi.ap.org/v2/categories.svc/?apiKey=%s"
	r = requests.get(base % APkey)
	soup = BeautifulSoup.BeautifulSoup(r.content)
	for entry in soup.findAll('entry'):
		name = str(entry.title.string)
		id = str(entry.id.string).split(':')[-1]
		yield "%s,%s" % (id, name)

""" ARTICLE SOURCES """
def AP_topNews(count=10):
	APkey = AP_keys["breaking-news"]
	category = 41664 # AP Online Top General Short Headlines
	contentOption = 0
	base = "http://developerapi.ap.org/v2/categories.svc/%d/?contentOption=%d&count=%d"\
		"&mediaOption=0&apiKey=%s"
	r = requests.get(base % (category, contentOption, count, APkey))
	soup = BeautifulSoup.BeautifulSoup(r.content)

	articles = []
	for entry in soup.findAll('entry'):
		url = str(entry.link["href"])
		title = str(entry.title.string)
		source = "Associated Press"
		pub_date = str(entry.updated.string.split('T')[0])
		
		tags = []
		tags.extend([str(cat['label']) for cat in entry.findAll('category')])
		
		a = Article(url, source, pub_date, map(str.lower, tags), title)
		if contentOption == 2: # if we get the source text with it, may as well use it
			entry_content = entry.findAll(attrs={"class":"entry-content"})[0].contents
			a.html = "".join(map(str, entry_content))
			a.text = " ".join(map(lambda x: re.sub(r'<[^>]+>', '', str(x)), entry_content))
		articles.append(a)
	return articles

def NYT_mostPopular(num_days=1, type="mostviewed", sec_list=["all-sections"]):
	""" Return a list of Article objects """
	#type = "mostemailed" / type = "mostshared"
	sections = ";".join(sec_list)
	base = "http://api.nytimes.com/svc/mostpopular/v2/%s/%s/%d.json"\
		"?api-key=32a8ad498501475cb0fa4abbc04f4e4e:5:61481359"
	r = requests.get(base % (type, sections, num_days))
	jresp = json.loads(r.content)
	
	articles = []
	for data in jresp["results"]:
		url = data["url"]
		title = data["title"]
		source = data["source"]
		pub_date = data["published_date"]
		
		# tags
		tags = []
		tags.extend(data["org_facet"]) # organizations
		for perstr in data["per_facet"]: # people
			fl = perstr.split(", ")
			if len(fl) == 2:
				last, first = perstr.split(", ")
				first = first.split()[0]
				tags.append(" ".join([first, last]))
			else:
				tags.append(perstr)
		tags.append(data["section"]) # newspaper section
		tags.extend(data["geo_facet"]) # geography
		tags.extend(data["des_facet"]) # NYT tags
		
		a = Article(url, source, pub_date, map(lambda x: x.encode('ascii').lower(), tags), title)
		articles.append(a)
	return articles

if __name__=="__main__":
	articles = NYT_mostPopular()
	articles.extend(AP_topNews())
	print "Latest Articles:"
	for a in articles:
		print "\t%s (%s, %s) - %s" % (a.title, a.source, a.pub_date, a.url)
		print "\t\t%s" % a.getAbstract()
		#_ = a.getHTML()
		#_ = a.getText()
	print ""
	print "Done"
