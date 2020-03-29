import flask
from flask import request, jsonify
import algorithm.vizener as vizener
from flask import Markup

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def homepage():
    return app.send_static_file('index.html')

@app.route('/encrypt/vizener', methods=['GET'])
def encryptVizener():
    if 'text' in request.args and 'key' in request.args:
        key = request.args['key']
        text = request.args['text']
    else:
        return "Error: You must provide text and key for encryption"

    return vizener.encrypt(text, key)

@app.route('/decrypt/vizener', methods=['GET'])
def decryptVizener():
   encrypted = request.args['encrypted']
   print(encrypted)
   return request.args['encrypted']

app.run()