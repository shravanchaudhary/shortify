import os
from flask import Flask, redirect, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://db:27017/')
db = client.urls

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

# db.urls.drop_index("createdAt_1")
# db.urls.create_index("createdAt", expireAfterSeconds=20)  
# print(db.urls.index_information())

def short_insert(url):
    tiny = db.url.insert_one({
        'url': url,
        'createdAt': datetime.now(),
        'clicks': 0
    }) 
    return 'http://localhost:5002/'+encode(str(tiny.inserted_id))

@app.route('/tiny/<url>')
def tiny(url):
    return short_insert(url)

@app.route('/tiny', methods=['POST'])
def tinyjson():
    url = request.json['url']
    return short_insert(url)

@app.route('/token/<path:varargs>')
def api(varargs=None):
    return varargs

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
