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
        output = data.get('output')

        playerId = data.get('playerInfo').get("id")
        playerName = data.get('playerInfo').get("playerName")

        return {
            "speech": output,
            # "data": data,
            "contextOut": [{"name":"context-player", "lifespan":1, "parameters":{"player-id": playerId}},{"name":"context-player", "lifespan":1, "parameters":{"player-name": playerName}}],
            "source": "apiai-weather-webhook-sample"
        }
    if req.get("result").get("action") == "context-player-salary":
        playerId = req.get("result").get("contexts")[0].get("parameters").get("player-id")
        playerName = req.get("result").get("contexts")[0].get("parameters").get("player-name")
        yql_url = "http://marcolemmens.com/ziggo/api.php?query=playerSalary&playerId=" + playerId+"&playerName=" + playerName
        result = urlopen(yql_url).read()
        data = json.loads(result)
        output = data.get('output')
        playerId = data.get('playerInfo').get("id")
        playerName = data.get('playerInfo').get("playerName")
        return {
            "speech": output,
            "data": playerName,
            "contextOut": [{"name":"context-player", "lifespan":1, "parameters":{"player-id": playerId}},{"name":"context-player", "lifespan":1, "parameters":{"player-name": playerName}}],
            "source": "apiai-weather-webhook-sample"
        }
    if req.get("result").get("action") == "context-player-length":
        playerId = req.get("result").get("contexts")[0].get("parameters").get("player-id")
        playerName = req.get("result").get("contexts")[0].get("parameters").get("player-name")
        yql_url = "http://marcolemmens.com/ziggo/api.php?query=playerLength&playerId=" + playerId+"&playerName=" + playerName
        result = urlopen(yql_url).read()
        data = json.loads(result)
        output = data.get('output')
        playerId = data.get('playerInfo').get("id")
        playerName = data.get('playerInfo').get("playerName")
        return {
            "speech": output,
            "data": playerName,
            "contextOut": [{"name":"context-player", "lifespan":1, "parameters":{"player-id": playerId}},{"name":"context-player", "lifespan":1, "parameters":{"player-name": playerName}}],
            "source": "apiai-weather-webhook-sample"
        }
    if req.get("result").get("action") == "specific-player":

        playerName = req.get("result").get("metadata").get("intentId")

        yql_url = "http://marcolemmens.com/ziggo/api.php?query=specificPlayerInfo&playerName=" + playerName
        result = urlopen(yql_url).read()
        data = json.loads(result)
        output = data.get('output')

        return {
            "speech": output,
            "data": playerName,
            "contextOut": [{"name":"context-player", "lifespan":1, "parameters":{"player-id": playerId}},{"name":"context-player", "lifespan":1, "parameters":{"player-name": playerName}}],
            "source": "apiai-weather-webhook-sample"
        }

    if req.get("result").get("action") == "last-event":

        yql_url = "http://marcolemmens.com/ziggo/api.php?query=lastEvent
        result = urlopen(yql_url).read()
        data = json.loads(result)
        output = data.get('output')

        eventName = data.get('eventInfo').get("eventName")

        return {
            "speech": output,
            "data": eventName,
            "contextOut": [{"name":"context-event", "lifespan":1, "parameters":{"event-name": eventName}}],
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
