from datetime import datetime
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
#run flask on linux amazon http://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/

from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
DATABASE_NAME = "databetes_app"
TABLE_NAME = "user_data"
db = client[DATABASE_NAME]
client_name = ""

import fatsecret_api

def add(dic):
	posts = db[TABLE_NAME]
	result = posts.insert_one(dic)
	print('One post: {0}'.format(result.inserted_id))

def update(user_id, dic):
	posts = db[TABLE_NAME]
	posts.update_many({"name": user_id}, {"$set": dic})

def retrieve(params, posts):
	post = posts.find_one(params)
	return post

@app.route('/')
def login():
	global client_name
	client_name = ""
	return render_template('login.html')

@app.route('/', methods=['POST'])
def login_post():
	global client_name
	client_name = request.form['name']
	if db[TABLE_NAME].find({'name': client_name}).count() <= 0:
		return redirect(url_for('new_user'))
	else:
		return redirect(url_for('main'))

@app.route('/new/')
def new_user():
	return render_template('new_user.html', username=client_name)

@app.route('/new/', methods=['POST'])
def new_user_input():
    global client_name
    gender = request.form['gender']
    age = request.form['age']
    race = request.form['race']
    if gender == "" or age == "" or race == "":
    	return "Invalid params"
    new_doc = {"name":client_name, "age":age, "gender":gender, "race":race}
    add(new_doc)
    return redirect(url_for('main'))

@app.route('/main/')
def main():
	global client_name
	# doc = retrieve({"author":"Brandon"}, db.posts)
	# print(doc)
	labels = ["January","February","March","April","May","June","July","August"]
	values = [10,9,8,7,6,4,7,8]
	scat_values = {1:6, 2:5, 3:4}
	return render_template('index.html', username=client_name, values=values, labels=labels, scatter_values=scat_values)

@app.route('/main/', methods=['POST'])
def my_form_post():
    food = request.form['food']
    serving_size = request.form['serving_size']
    if food == "" or serving_size == "":
    	return "Invalid Inputs!"

    #current_time = str(datetime.now())
    queries = fatsecret_api.search_food(food)
    food_names = []
    for food_data in queries:
    	food_names.append(food_data["food_name"])

    labels = ["January","February","March","April","May","June","July","August"]
    values = [10,9,8,7,6,4,7,8]
    scat_values = {1:6, 2:5, 3:4}
    return render_template('choose_food.html', results=food_names, username=client_name, values=values, labels=labels, scatter_values=scat_values)

if __name__ == "__main__":
	app.run(debug=True)