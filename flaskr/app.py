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
DIABETES_SET_TABLE = "diabetes_data_set"
db = client[DATABASE_NAME]
client_name = ""

import fatsecret_api
import fatsecret_crawl

def add(dic):
	posts = db[TABLE_NAME]
	result = posts.insert_one(dic)

def update(user_id, dic):
	posts = db[TABLE_NAME]
	posts.update_many({"name": user_id}, {"$set": dic})

def retrieve(user_id, posts):
	post = posts.find_one({"name": user_id})
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
    new_doc = {"name":client_name, "age":age, "gender":gender, "race":race, "carb_log":{}, "serv_log":{}}
    add(new_doc)
    return redirect(url_for('main'))

@app.route('/main/')
def main():
	global client_name
	# doc = retrieve({"author":"Brandon"}, db.posts)
	# print(doc)
	labels = ["January","February","March","April","May","June","July","August"]
	values = [10,9,8,7,6,4,7,8]

	self_data = retrieve(client_name, db[TABLE_NAME])
	self_race = self_data['race']
	self_gender = self_data['gender']
	diabetes_db_data = db[DIABETES_SET_TABLE].find_one({"race/gender":self_race.lower()+","+self_gender.lower()})
	diabetes_graph = diabetes_db_data['graph']
	a1c = diabetes_graph['a1c']
	age = diabetes_graph['age']
	scat_values = []
	for i in range(len(a1c)):
		if age[i] == 0:
			continue
		scat_values.append([a1c[i], age[i]])

	return render_template('index.html', username=client_name, values=values, labels=labels, scatter_values=scat_values)

@app.route('/main/', methods=['POST'])
def my_form_post():
    global queries
    food = request.form['food']
    if food == "":
    	return "Invalid Inputs!"

    #current_time = str(datetime.now())
    queries = fatsecret_api.search_food(food)

    return redirect(url_for('choose_food'))

@app.route('/choose_food/')
def choose_food():
	global client_name, queries
	labels = ["January","February","March","April","May","June","July","August"]
	values = [10,9,8,7,6,4,7,8]
	scat_values = {1:6, 2:5, 3:4}

	food_names = []
	for food_data in queries:
		food_names.append(food_data["food_name"])

	return render_template('choose_food.html', results=food_names, username=client_name, values=values, labels=labels, scatter_values=scat_values)

@app.route('/choose_food/', methods=['POST'])
def choose_food_post():
	global client_name, queries
	food_name = request.form['type_food']
	serving_size = request.form['serving_size']
	if serving_size == "":
		return "Invalid Inputs!"
	data = {}
	for food_data in queries:
		if food_name == food_data["food_name"]:
			data = food_data

	url = data['food_url']
	carbs_per_serv = float(fatsecret_crawl.get_carb_per_serving(url))
	total_carbs = int(float(serving_size) * carbs_per_serv *100)/100
	current_time = str(datetime.now()).split(" ")[0]
	old = retrieve(client_name, db[TABLE_NAME])
	old_carbs = old['carb_log']
	old_serv = old['serv_log']
	old_carbs[current_time] = total_carbs
	old_serv[current_time] = serving_size

	update(client_name, {"carb_log":old_carbs, "serv_log":old_serv})
	
	return redirect(url_for('main'))

if __name__ == "__main__":
	app.run(debug=True)