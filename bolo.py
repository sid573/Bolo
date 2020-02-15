from flask import Flask
from parsel import * 
app = Flask(__name__)

@app.route('/<gender>/<int:track_id>')
def hello_world(gender,track_id):
    y = bolo_host(gender,track_id)
    return y

# @app.route('/uploadfile',methods=['GET','POST'])
# def uploadfile():
#     if request.method == 'PUT':
#     	f = request.files['file']
#         filePath = "./somedir/"+secure_filename(f.filename)
#         f.save(filePath)
#         return "success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
