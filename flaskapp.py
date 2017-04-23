from flask import Flask, jsonify
from flask import request
import maps
import replyNexmo as reply
import bot
import wiki
import trial
# import quickstart
import subprocess as command
# import twit
# from googleapiclient.discovery import build

import searchGoogle

mode = "text"
randomT = "Hi this is a trial custom message developed by few folks at Rutgers. Hope this comes out well."

# print output

app = Flask(__name__)
number = 0
messageReceived = ""





@app.route('/')
def test():
	return "Hello from the other side!"

@app.route('/sms/', methods=['GET', 'POST'])
def something():
	global number
	global mode
	global randomT
	data = request.get_json(silent=True)
	print "raw: ", data
	number = data['msisdn']
	messageReceived = data['text']
	print "From: ", number
	parsed_key = bot.getKey(messageReceived)
	if messageReceived == "mode: voice":
		mode = "voice"
	else:
		mode ="text"
	print ("Mode: ", mode)
	if parsed_key["result"]["metadata"]:
		print parsed_key["result"]["metadata"]["intentName"]
		if parsed_key["result"]["metadata"]["intentName"] == "directions":
			start = parsed_key["result"]["parameters"]["start"]
			end = parsed_key["result"]["parameters"]["end"]
			directions = maps.getDirections(start, end)
			print directions
			if mode == "text":
				reply.send_sms(number, directions)
			else:
				randomT = directions
				trial.make_call(number)
		elif parsed_key["result"]["metadata"]["intentName"] == "summary":
			searchTerm = parsed_key["result"]["parameters"]["text"]
			# searchRes = "Sorry, didn't follow that"
			# if (searchTerm):
			# searchRes = wiki.searchWiki(searchTerm)
			searchRes = searchGoogle.parse_results(searchTerm)
			if mode == "text":
				reply.send_sms(number, searchRes)
			else:
				randomT = searchRes
				trial.make_call(number)
		elif parsed_key["result"]["metadata"]["intentName"] == "twitterread":
			tweets = command.Popen("/home/ubuntu/flaskapp/twit.sh", stdout=command.PIPE, shell=True)
			(output, err) = tweets.communicate()
			tweets_status = tweets.wait()
			print output
			if mode == "text":
				print reply.send_sms(number, output)
			else:
				randomT = output
				trial.make_call(number)
		# 	n = parsed_key["result"]["parameters"]["content"]

		elif parsed_key["result"]["metadata"]["intentName"] == "mailread":
			# from googleapiclient.discovery import build

			# mail = command.Popen("/home/ubuntu/flaskapp/mail.sh", stdout=command.PIPE, shell=True)
			mail = command.Popen("python /home/ubuntu/flaskapp/quickstart.py", stdout=command.PIPE, shell=True)
			(output, err) = mail.communicate()
			mail_status = mail.wait()
			print output
			if mode == "text":
				print reply.send_sms(number, output)
			else:
				trial.make_call(number)
		else:
			if mode == "text":
				print reply.send_sms(number, parsed_key["result"]["fulfillment"]["speech"])
			else:
				randomT = parsed_key["result"]["fulfillment"]["speech"]
				trial.make_call(number)


	else:
		if mode == "text":
			print reply.send_sms(number, parsed_key["result"]["fulfillment"]["speech"])
		else:
			randomT = parsed_key["result"]["fulfillment"]["speech"]
			trial.make_call(number)
		


	# reply.send_sms(number, "Successfully received: " + messageReceived)
	# if "search" in messageReceived:
	# 	print "Seqrch"
	# 	print maps.getDirections("7C Smith Street, Boston", "902 Huntington Ave, Boston")

	
	#app.logger.debug('%s',request.get_data())	
	return jsonify({201: "OK"})
	#return (201,"SUCCESS")

@app.route('/calls', methods = ['GET',  'POST'])
def do_call():
	# data = request.get_json(silent=True)
	# print "CALLS", data
	global randomT
	# return jsonify({"action": "talk", "voiceName":"Russell", "text":randomT })
	return (jsonify([
	    {
	        "action": "talk",
	        "voiceName": "Russell",
	        "text": randomT
	    }
	]))

if __name__ == '__main__':
	app.run(debug=True)
