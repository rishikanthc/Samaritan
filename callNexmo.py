import time
import BaseHTTPServer
import json
import requests
from datetime import datetime
from base64 import urlsafe_b64encode
import os
import calendar
from jose import jwt
# from application_generate_jwt import generate_jwt
import ConfigParser



HOST_NAME = 'example.net' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80 # Maybe set this to 9000.







class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        #Parse parameters in the GET request
        parsed_path = urlparse(s.path)
        try:
                params = dict(
                [p.split('=') for p in parsed_path[4].split('&')])
        except:
                params = {}

        #Retrieve with the parameters in this request
        call_to = params['to']      #The endpoint being called
        call_form = params['from']  #The endpoint you are calling from
        call_uuid = params['conversation_uuid']     #The unique ID for this Conversation

        #Dynamically create the NCCO to run a conversation from your virtual number
        if call_to == "16504954796":
            ncco=[
            {
                "action": "talk",
                "text": "Hello Russell, welcome to a Call made with Voice API"
                }
            ]
        else:
            ncco=[
            {
                "action": "talk",
                "text": "Hello Rebekka, welcome to a Call made with Voice API"
                }
            ]

        #For more advanced Conversations you use the paramaters to personalize the NCCO
        #Dynamically create the NCCO to run a conversation from your virtual number

        print "GET Request from " + s.path
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(json.dumps(ncco))

    def do_POST(s):
        """Parse parameters in the POST request"""
        content_len = int(s.headers.getheader('content-length', 0))
        post_body = s.rfile.read(content_len)
        inbound_message = json.loads(post_body.decode('utf-8'))

        # Check if your messages are successful
        if inbound_message['status'] == 'ringing':
            print ("Handle conversation_uuid, this return parameter identifies the Conversation")
        if inbound_message['status'] == 'answered':
            print ("You use the uuid returned here for all API requests on individual calls")
        if inbound_message['status'] == 'complete':
            print ("Find your recording")
            #if you set eventUrl in your NCCO. The recording download URL
            #is returned in recording_url. It has the following format
            # https://api.nexmo.com/media/download?id=52343cf0-342c-45b3-a23b-ca6ccfe234b0
            #Make a GET request to this URL using a JWT as authentication to download
            #the Recording. For more information, see Recordings.
        """Tell Nexmo that you have recieved the POST request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

def generate_jwt(application_id="none", keyfile="key.txt") :

    application_private_key = open(keyfile, 'r').read()
    # Add the unix time at UCT + 0
    d = datetime.utcnow()

    token_payload = {
        "iat": calendar.timegm(d.utctimetuple()),  # issued at
         "application_id": application_id,  # application id
         "jti": urlsafe_b64encode(os.urandom(64)).decode('utf-8')
    }

    # generate our token signed with this private key...
    return jwt.encode(
        claims=token_payload,
        key=application_private_key,
        algorithm='RS256')



base_url = "http://52.11.94.232"
# version = "/v1"
version = ""
action = "/calls"

#Application and call information
application_id = "324c9d42-c606-43e2-8231-9ebc9d5e85d9"
keyfile = "key.txt"
# keyfile = "private.key"
#Create your JWT
jwt = generate_jwt(application_id, keyfile)

#Create the headers using the jwt
headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer {0}".format(jwt)
}

#Change the to parameter to the number you want to call
payload = {
    "to":[{
        "type": "phone",
        "number": "16054954796"
    }],
    "from": {
        "type": "phone",
        "number": "12034869034"
    },
    "answer_url": ["https://nexmo-community.github.io/ncco-examples/first_call_talk.json"]
}



response = requests.post( base_url + version + action , data=json.dumps(payload), headers=headers)

if (response.status_code == 201):
    print response.content
else:
    print( "Error: " + str(response.status_code) + " " +    response.content)
# if __name__ == '__main__':
#     server_class = BaseHTTPServer.HTTPServer
#     httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
#     print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
#     try:
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         pass
#     httpd.server_close()
#     print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
