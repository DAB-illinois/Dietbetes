from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)

db = client.pymongo_test

def add(dic):
	posts = db.posts
	result = posts.insert_one(dic)
	print('One post: {0}'.format(result.inserted_id))

def retrieve(params, posts):
	post = posts.find_one(params)
	print(post)

post_data = {
	'title': 'Python and MongoDB',
	'content': 'PyMongo is fun, you guys',
	'author': 'Brandon'
}

retrieve_data = {'author': 'Brandon'}