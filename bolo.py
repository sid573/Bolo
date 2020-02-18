from flask import Flask, flash, request, redirect, url_for, jsonify
from parsel import * 
from werkzeug.utils import secure_filename
app = Flask(__name__)

# @app.route('/<gender>/<int:track_id>')
# def hello_world(gender,track_id):
#     y = bolo_host(gender,track_id)
#     return y

@app.route('/uploadfile',methods=['GET','POST'])
def uploadfile():
    if request.method == 'POST':
        f = request.files['file']
        filePath = secure_filename(f.filename)
        f.save(filePath)
        y = bolo_host("M",1,f.filename)
        return y
    elif request.method == 'GET':
        y = bolo_host("M",1,"output.wav")
        return y

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
