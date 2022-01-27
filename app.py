from bson.objectid import ObjectId
from flask import Flask, json, render_template
import requests
from flask_pymongo import PyMongo
import pandas as pd
from bson.json_util import dumps
from pandas import DataFrame
from flask import jsonify, request
from werkzeug.utils import redirect
import matplotlib.pyplot as plt
from pymongo import MongoClient


app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/koreantv"
mongo = PyMongo(app)

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    return render_template('AAT.html')

@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _title = _json['title']
    _rating = float(_json['rating'])
    _votes = int(_json['votes'])
    _time = _json['time']
    _genre = _json['genre']
    _stars = _json['stars']

    if _title and _rating and _votes and _time and _genre and _stars and request.method == 'POST':
        id = mongo.db.kdrama.insert_one({'Title': _title, 'Rating': _rating, 'Votes': _votes, 'Time': _time, 'Genre': _genre, 'Stars': _stars})
        resp = jsonify("Show has been added successfully")
        resp.status_code = 200
        return resp

    else:
        return not_found()

@app.route('/shows')
def shows():
    show = mongo.db.kdrama.find()
    resp = dumps(show)
    return resp

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
    mongo.db.kdrama.delete_one({'_id': ObjectId(id)})
    resp = jsonify("Show deleted successfully")
    resp.status_code = 200
    return redirect('/')
    return resp

@app.route('/update/<id>', methods=['POST', 'GET'])
def update_game(id):
    if request.method == 'POST':
        _id = id
        _title = request.form['title']
        _rating = float(request.form['rating'])
        _votes = int(request.form['votes'])
        _time = request.form['time']
        _genre = request.form['genre']
        _stars = request.form['stars']

        if _title and _rating and _votes and _time and _genre and _stars and request.method == 'POST':
            id = mongo.db.kdrama.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set':  {'Title': _title, 'Rating': _rating, 'Votes': _votes, 'Time': _time, 'Genre': _genre, 'Stars': _stars}})
            resp = jsonify("Show updated successfully")
            resp.status_code = 200
            return redirect('/')
            return resp
        else:
            return not_found()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        req = requests.get('http://127.0.0.1:80/shows')
        data = json.loads(req.content)
        return render_template('index.html', data=data)
    elif request.method == 'POST':
        _title = request.form['title']
        _rating = float(request.form['rating'])
        _votes = int(request.form['votes'])
        _time = request.form['time']
        _genre = request.form['genre']
        _stars = request.form['stars']
        if _title and _rating and _votes and _time and _genre and _stars and request.method == 'POST':
            id = mongo.db.kdrama.insert_one({'Title': _title, 'Rating': _rating, 'Votes': _votes, 'Time': _time, 'Genre': _genre, 'Stars': _stars})
            resp = jsonify("Show added successfully")
            resp.status_code = 200
            return redirect('/')
        else:
            return not_found()

@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status' : 404,
        'message' : 'Not Found '+ request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(port=80, debug=True)
