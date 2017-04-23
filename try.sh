#!/bin/bash
curl 'https://rest.nexmo.com/call/json' \
-d api_key="3675d142" \
-d api_secret="a0eab3f1295ce225" \
-d to="3476155327" \
--data-urlencode answer_url="https://nexmo-community.github.io/ncco-examples/first_call_talk.json" \
-d from="12034869034"
