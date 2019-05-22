import os
from flask import Flask, redirect, jsonify
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


# db.urls.drop_index("createdAt_1")
# db.urls.create_index("createdAt", expireAfterSeconds=20)  
# print(db.urls.index_information())
@app.route('/<tiny>')
def todo(tiny):
    object_id = ObjectId(decode(tiny))
    url = url_coll.find_one({"_id": object_id})
    if url == None:
        return "Url not found"
    return jsonify({
        'url': url['url'],
        'clicks': str(url['clicks'])
        })
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)