from flask import Flask, jsonify
from flask import request
import maps

app = Flask(__name__)
number = 0
messageReceived = ""


@app.route('/')
def test():
	return "Hello from the other side!"

@app.route('/sms/', methods=['GET', 'POST'])
def something():
	global number
	global messageReceived
	data = request.get_json(silent=True)
	number = data['msisdn']
	messageReceived = data['text']
	print "Message: ", messageReceived, "From: ", number
	
	#app.logger.debug('%s',request.get_data())	
	return jsonify({201: "OK"})
	#return (201,"SUCCESS")

@app.route('/calls', methods = ['GET',  'POST'])
def do_call():
	data = request.get_json(silent=True)
	print "CALLS", data
	return jsonify({"status_code": 201})

if __name__ == '__main__':
	app.run(debug=True)
