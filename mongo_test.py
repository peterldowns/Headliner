import pymongo
from pymongo import Connection
# see http://docs.dotcloud.com/guides/environment/ for ENV access
#   for accessing a mongodb's user/pass data

host = 'localhost'
port = 27017
connection = Connection(host, port)

db = connection['news']
test_article = {"source" : None, 	# where it came from
		   "url" : None,		# article URL
		   "pub_date" : None,	# date published
		   "tags" : None,		# list of tags
		   "title" : None,		# article title
		   "html" : None,		# the cleaned HTML of the article
		   "value" : None }		# how much I'd like it, based on keywords / sources (?)
articles = db.articles
# or, for capped collections (at most /size/ documents, insert-ordered)
# db.createCollection("articles", {"capped":True, "size":500})
# articles = db.articles

articles.insert(test_article) # accepts an iterable for bulk insertion, too

for post in articles.find({"url" : None})  # search for multiple articles
	out = post
	print out

out = articles.find_one({"url": None}) # search for a single article
print out

num = articles.count()
print "There are %d articles in the database" % num

num_none = articles.find({"url":None}).count() # count works for searches, too
print "There are %d articles where url=None" % num_none
