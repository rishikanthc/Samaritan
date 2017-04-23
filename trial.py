import nexmo


# # root = os.path.dirname("__file__")
# with open("key.pem", 'r') as rsa_priv_file:

#     #Not sure about adding the utf-8 AT ALL
#     priv_rsakey = rsa_priv_file.read()

# client = nexmo.Client(key="3675d142", secret="a0eab3f1295ce225", application_id="324c9d42-c606-43e2-8231-9ebc9d5e85d9", private_key=priv_rsakey)

# response = client.create_call({
#   'to': [{'type': 'phone', 'number': '13476155327'}],
#   'from': {'type': 'phone', 'number': '12034869034'},
#   'answer_url': ['https://nexmo-community.github.io/ncco-examples/first_call_talk.json']
# })

# print ("response is", response)
# response = client.get_calls()
# print ("calls: ", response)
import json
import requests
from datetime import datetime
from base64 import urlsafe_b64encode
import os
import calendar
from jose import jwt

def generate_jwt(application_id="324c9d42-c606-43e2-8231-9ebc9d5e85d9", keyfile="./key.txt") :

    application_private_key = open(keyfile, 'r').read()
    # application_private_key = ""
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


pkey = open('test/private_key.txt').read()
client = nexmo.Client(
	key="3675d142",
	secret="a0eab3f1295ce225",
	application_id="324c9d42-c606-43e2-8231-9ebc9d5e85d9",
	private_key=pkey
)

response = client.create_call({
	'to': [{'type': 'phone', 'number': 13476155327}],
	'from': {'type': 'phone', 'number': 12034869034},
	'answer_url': ['https://nexmo-community.github.io/ncco-examples/first_call_talk.json']
})

print response
