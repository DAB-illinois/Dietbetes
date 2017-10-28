from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

#run flask on linux amazon http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
DATABASE_NAME = "databetes_app"
TEST_DATABASE_NAME = "pymongo_test"

db = client[TEST_DATABASE_NAME]

def retrieve(params, posts):
	post = posts.find_one(params)
	return post

@app.route('/')
def my_form():
	doc = retrieve({"author":"Brandon"}, db.posts)
	print(doc)
	return render_template("index.html", title=doc["title"], author=doc["author"])

if __name__ == "__main__":
	app.run(debug=True)