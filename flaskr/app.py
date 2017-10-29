from datetime import datetime
import random
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
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

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

import key

app.config['GOOGLEMAPS_KEY'] = key.GOOGLE_MAPS_KEY
app.config['SECRET_KEY'] = str(random.random())
GoogleMaps(app)

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
	if client_name == "":
		return redirect(url_for('login'))

	if db[TABLE_NAME].find({'name': client_name}).count() <= 0:
		return redirect(url_for('new_user'))
	else:
		resp = make_response(redirect(url_for('main')))
		resp.set_cookie("user", client_name)
		return resp

@app.route('/new/')
def new_user():
	if client_name == "":
		return redirect(url_for('login'))
	return render_template('new_user.html', username=client_name)

@app.route('/new/', methods=['POST'])
def new_user_input():
	global client_name
	if "gender" not in request.form or "age" not in request.form or "race" not in request.form:
		return "Invalid params"
	gender = request.form['gender']
	age = request.form['age']
	race = request.form['race']
	new_doc = {"name":client_name, "age":age, "gender":gender, "race":race, "carb_log":{}, "serv_log":{}}
	add(new_doc)
	resp = make_response(redirect(url_for('main')))
	resp.set_cookie("user", client_name)
	return resp

@app.route('/main/')
def main():
	global carb_labels, carb_values, serv_values, serv_labels, scat_values
	client_name = request.cookies.get('user')

	if client_name == "":
		return redirect(url_for('login'))

	history = retrieve(client_name, db[TABLE_NAME])

	carb_hist = history['carb_log']
	carb_labels = []
	carb_values = []
	for i in carb_hist:
		carb_labels.append(i)
	carb_labels.sort()
	for i in carb_labels:
		carb_values.append(carb_hist[i])
	session['carb_labels'] = carb_labels
	session['carb_values'] = carb_values

	serv_hist = history['serv_log']
	serv_labels = []
	serv_values = []
	for i in serv_hist:
		serv_labels.append(i)
	serv_labels.sort()
	for i in serv_labels:
		serv_values.append(serv_hist[i])
	session['serv_labels'] = serv_labels
	session['serv_values'] = serv_values

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
	session['scat_values'] = scat_values

	return render_template('index.html', username=client_name, scatter_values=scat_values, carb_labels=carb_labels, carb_values=carb_values, serv_labels=serv_labels, serv_values=serv_values)

@app.route('/main/', methods=['POST'])
def my_form_post():
	if request.cookies.get('user') == "":
		return redirect(url_for('login'))

	food = request.form['food']
	if food == "":
		return "Invalid Inputs!"

	queries = fatsecret_api.search_food(food)
	session['queries'] = queries

	return redirect(url_for('choose_food'))

@app.route('/choose_food/')
def choose_food():
	if request.cookies.get('user') == "":
		return redirect(url_for('login'))

	food_names = []
	for food_data in session.get('queries', None):
		food_names.append(food_data["food_name"])

	return str(session.get('serv_labels', None))
	return render_template('choose_food.html', results=food_names, username=request.cookies.get('user'), scatter_values=session.get('scat_values', None), carb_labels=session.get('carb_labels', None), carb_values=session.get('carb_values', None), serv_labels=session.get('serv_labels', None), serv_values=session.get('serv_values', None))

@app.route('/choose_food/', methods=['POST'])
def choose_food_post():
	if request.cookies.get('user') == "":
		return redirect(url_for('login'))

	queries = session.get('queries', None)
	food_name = request.form['type_food']
	serving_size = int(request.form['serving_size'])
	if serving_size == "":
		return "Invalid Input!"
	data = {}
	for food_data in queries:
		if food_name == food_data["food_name"]:
			data = food_data

	url = data['food_url']
	carbs_per_serv = float(fatsecret_crawl.get_carb_per_serving(url))
	total_carbs = int(float(serving_size) * carbs_per_serv *100)/100
	current_time = str(datetime.now()).split(" ")[0]
	old = retrieve(request.cookies.get('user'), db[TABLE_NAME])
	old_carbs = old['carb_log']
	old_serv = old['serv_log']
	if current_time in old_carbs:
		old_carbs[current_time] += total_carbs
		old_serv[current_time] += serving_size
	else:
		old_carbs[current_time] = total_carbs
		old_serv[current_time] = serving_size

	update(request.cookies.get('user'), {"carb_log":old_carbs, "serv_log":old_serv})
	
	return redirect(url_for('main'))

@app.route("/map/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    
    return render_template('map.html', mymap=mymap)

if __name__ == "__main__":
	app.run(debug=True, threaded=True)