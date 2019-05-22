import os
from flask import Flask, redirect, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://db:27017/')
db = client['shortify']
url_coll = db['urls']

base = {}
rbase = {}

for i in range(10):
    base[i] = str(i)
for i in range(10,36):
    base[i] = chr(i - 10 + ord('a'))
for i in range(36,62):
    base[i] = chr(i - 36 + ord('A'))
base[62] = '_'
base[63] = '-'

for x,y in base.items():
    rbase[y] = x

def tobase(number, to):
    num = ''
    if number == to:
        return '10'
    while number > 0:
        num += base[number % to]
        number //= to
    return num[::-1]

def todec(number, frm):
    num = 0
    for x in number:
        num *= frm
        num += rbase[x]
    return num

def encode(id):
    dec = todec(id, 16)
    return tobase(dec, 64)

def decode(tiny):
    dec = todec(tiny, 64)
    return tobase(dec, 16)

# Created expiration time for 60 seconds for testing purpose
db.urls.drop_index("createdAt_1")
url_coll.ensure_index("createdAt", expireAfterSeconds=15)  
# print(db.urls.index_information())

def short_insert(url):
    tiny = url_coll.insert_one({
        'url': url,
        'createdAt': datetime.now(),
        'clicks': 0
    }) 
    encoded_url = encode(str(tiny.inserted_id))
    return jsonify({
    	'short_url': 'http://localhost:5002/'+encoded_url,
    	'stats': 'http://localhost:5003/'+encoded_url
    	})

@app.route('/<url>')
def tiny(url):
    return short_insert(url)

@app.route('/', methods=['POST'])
def tinyjson():
    url = request.json['url']
    return short_insert(url)

@app.route('/settings/expiry/<seconds>')
def set_expiry_time(seconds):
	url_coll.drop_index("createdAt_1")
	url_coll.ensure_index("createdAt", expireAfterSeconds=int(seconds))
	return 'updated expiry time'  


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
