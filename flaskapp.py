from flask import Flask, jsonify
from flask import request
import maps
import replyNexmo as reply
import bot
import wiki
# from googleapiclient.discovery import build

# import searchGoogle

app = Flask(__name__)
number = 0
messageReceived = ""


@app.route('/')
def test():
	return "Hello from the other side!"

@app.route('/sms/', methods=['GET', 'POST'])
def something():
	global number
	
	data = request.get_json(silent=True)
	print "raw: ", data
	number = data['msisdn']
	messageReceived = data['text']
	print "From: ", number
	parsed_key = bot.getKey(messageReceived)
	if parsed_key["result"]["metadata"]:
		print parsed_key["result"]["metadata"]["intentName"]
		if parsed_key["result"]["metadata"]["intentName"] == "directions":
			start = parsed_key["result"]["parameters"]["start"]
			end = parsed_key["result"]["parameters"]["end"]
			directions = maps.getDirections(start, end)
			print directions
			reply.send_sms(number, directions)
		elif parsed_key["result"]["metadata"]["intentName"] == "summary":
			searchTerm = parsed_key["result"]["parameters"]["text"]
			# searchRes = "Sorry, didn't follow that"
			# if (searchTerm):
			searchRes = wiki.searchWiki(searchTerm)
			reply.send_sms(number, searchRes)
		else:
			print reply.send_sms(number, parsed_key["result"]["fulfillment"]["speech"])


	else:
		print reply.send_sms(number, parsed_key["result"]["fulfillment"]["speech"])
		


	# reply.send_sms(number, "Successfully received: " + messageReceived)
	# if "search" in messageReceived:
	# 	print "Seqrch"
	# 	print maps.getDirections("7C Smith Street, Boston", "902 Huntington Ave, Boston")

	
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
