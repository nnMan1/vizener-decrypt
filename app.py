import flask
from flask import request, jsonify
import algorithm.vizener as vizener

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

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