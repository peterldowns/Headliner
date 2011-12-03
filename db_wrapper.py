from pymongo import Connection # for accessing the database
import json	# for loading the env file

def loadCredentials(env_path='/home/dotcloud/environment.json'):
	# Get DB information / credentials from an env file
	credentials = {}
	with open(env_path) as f:
		env = json.load(f)
	credentials['host'] = env['DOTCLOUD_DB_MONGODB_HOST']
	credentials['port'] = env['DOTCLOUD_DB_MONGODB_PORT']
	credentials['user'] = env['DOTCLOUD_DB_MONGODB_LOGIN']
	credentials['pass'] = env['DOTCLOUD_DB_MONGODB_PASSWORD']
	return credentials

def getDatabase(db_name, credentials=None):
	if not credentials:
		credentials = loadCredentials()
	# Load the admin database and authenticate
	connection = Connection(credentials['host'], int(credentials['port']))
	db = connection['admin']
	db.authenticate(credentials['user'], credentials['pass'])
	
	db = connection[db_name]
	return db

def getCollection(db_name, coll_name, credentials=None):
	db = getDatabase(db_name, credentials)
	return db[coll_name]

def addArticles(db_name, coll_name, articles, credentials=None):
	# expects articles as an iterable
	coll = getCollection(db_name, coll_name, credentials)
	return coll.insert(articles)


def searchCollection(db_name, coll_name, params=None, sort_params=None, credentials=None):
	coll = getCollection(db_name, coll_name, credentials)

	if params:
		resp = coll.find(params)
	else:
		resp = coll.find()
	
	if sort_params:
		return resp.sort(sort_params)
	return resp

def getLatest(db_name, coll_name, num, credentials=None):
	return searchCollection(db_name, coll_name, sort_params=["$natural",-1]).limit(num)
