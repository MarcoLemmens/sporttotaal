#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") == "context-player":
        yql_url = "http://marcolemmens.com/ziggo/api.php?query=playerInfo"
        result = urlopen(yql_url).read()
        data = json.loads(result)
        playerName = data.get('playerName')

        return {
            "speech": playerName,
            "displayText": playerName,
            # "data": data,
            "contextOut": [{"name":"context-player", "lifespan":1, "parameters":{"player-name":data.get('playerName')}}],
            "source": "apiai-weather-webhook-sample"
        }
    if req.get("result").get("action") == "context-player-salary":
        playerName = req.get("result").get("contexts")[0].get("parameters").get("player-name")
        yql_url = "http://marcolemmens.com/ziggo/api.php?query=playerInfo&playerName="
        result = urlopen(yql_url).read()
        data = json.loads(result)
        salary = data.get('salary')

        return {
            "speech": salary,
            "displayText": salary,
            "data": playerName,
            "contextOut": [{"name":"context-player", "lifespan":1, "parameters":{"player-name":data.get('playerName')}}],
            "source": "apiai-weather-webhook-sample"
        }
    if req.get("result").get("action") == "context-player-length":
        playerName = req.get("result").get("contexts")[0].get("parameters").get("player-name")
        yql_url = "http://marcolemmens.com/ziggo/api.php?query=playerInfo&playerName="
        result = urlopen(yql_url).read()
        data = json.loads(result)
        length = data.get('length')

        return {
            "speech": playerName + "is " + length + "cm tall",
            "displayText": playerName + "is " + length + "cm tall",
            "data": playerName,
            "contextOut": [{"name":"context-player", "lifespan":1, "parameters":{"player-name":data.get('playerName')}}],
            "source": "apiai-weather-webhook-sample"
        }
    else:
        return {}


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "That would be Eden Hazard"

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
