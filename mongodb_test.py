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
	return post

def update(user_id, dic):
	posts = db.posts
	posts.update_many({"author": user_id}, dic)

post_data = {
	'title': 'Python and MongoDB',
	'content': 'PyMongo is fun, you guys',
	'author': 'Brandon'
}

retrieve_data = {'author': 'Brandon'}