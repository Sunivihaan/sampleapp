#
from flask import Flask, render_template
import json
import urllib.request
import base64

# urllib.error.URLError
# urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)>
# https://shinespark.hatenablog.com/entry/2015/12/06/100000
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

application  = Flask(__name__)

# constant
my_Flask_url = "http://127.0.0.1:5000/"
api_endpoint_url = "https://eu-gb.dynamic-dashboard-embedded.cloud.ibm.com/daas"
client_id = "a05d92cd-704f-4a21-b8c8-cd82b2da88f6"
client_secret = "8f541030178d588d538acf893e6ac8d11689801e"

@application.route("/")
def index():
    client = client_id+":"+client_secret
    encoded_client = base64.b64encode(client.encode('utf-8')).decode('utf-8')
    url = api_endpoint_url+'/v1/session'
    data = {
      "expiresIn": 3600,
      "webDomain": my_Flask_url
    }
    headers = {
        'Content-Type': 'application/json',
        'authorization': 'Basic ' + encoded_client
    }

    req = urllib.request.Request(url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        body = res.read().decode('utf-8')
        body = json.loads(body)
    #print(body["sessionId"])
    #print(body["sessionCode"])
    return render_template('index.html', 
            sessionCode = body["sessionCode"])

if __name__ == "__main__":
    application .run(host='127.0.0.1')
