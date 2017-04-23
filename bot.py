import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'b1e86d8abb714f6d9b3e95f9dd40dd19'

session = "user session id"

# query = "search for barack obama"

def getKey(query):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'  # optional, default value equal 'en'

    request.session_id = session

    request.query = query

    response = request.getresponse()
    r =  json.loads(response.read())
    print r["result"]["fulfillment"]["speech"]
    print r["result"]
    return r
    # print r['result']
    # print r['metadata']
    # data = json.load(response)
    # print data["metadata"]
    # print (response.read())


if __name__ == '__main__':
    getKey("Hi")
