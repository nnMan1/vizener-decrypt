import flask
from flask import request, jsonify
import algorithm.vizener as vizener
from flask import Markup

app = flask.Flask(__name__)sudo snap install --classic heroku
app.config["DEBUG"] = True

@app.route('/favicon.ico', methods=['GET'])
def homepage():
    return "Test"

@app.route('/', methods=['GET'])
def homepage():
    return "Test"
    #return app.send_static_file('index.html')

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
   if 'encrypted' in request.args: 
       encrypted = request.args['encrypted']
   else:
       return "Error: Yout must provide text for decryption"

   return vizener.decrypt(encrypted)

app.run(host= '0.0.0.0')