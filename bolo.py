from flask import Flask
from parsel import * 
app = Flask(__name__)

@app.route('/<gender>/<int:track_id>')
def hello_world(gender,track_id):
    y = bolo_host(gender,track_id)
    return y