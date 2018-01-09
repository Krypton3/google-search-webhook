import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

from googleapiclient.discovery import build


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request: ")
    print(json.dumps(req, indent=4))
    res = MakeWebRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']


def makeWebhookResult(data, searchstring):
    if (data[0] is None):
        return {}

    articleUrl = data[0].get('formattedUrl')
    # print(json.dumps(item, indent=4))

    speech = "Please view this article for more information on " + searchstring + ": " \
             + articleUrl

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "google-search-webhook"
    }


def MakeWebRequest(req):
    if req.get("result").get("action") == "interest":
        result = req.get("result")
        parameters = result.get("parameters")
        names = parameters.get("org-name")
        organization = {'org1': '10', 'org2': '20', 'org3': '30'}
        speech = "The organization's of " + names + " small projects are: " + str(organization)
        print("Response: ")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            "source": "Athena"
        }
    elif req.get("result").get("action") != "googleSearch":
        json_params = req.get("result").get("parameters")
        searchstring = ''  # this creates the overall topic which covers user's raw query

        for value in json_params.values():
            searchstring += value
            searchstring += " "
        print(searchstring)
        searchString = "robot %s" % searchstring

        # KEYS SHOULDNT BE DISPLAYED
        my_api_key = ""
        my_cse_id = ""
        searchResults = google_search(searchString, my_api_key, my_cse_id, num=1)  # search for the topic

        if searchResults is None:
            return {}

        res = makeWebhookResult(searchResults, searchstring)
        return res
    elif req.get("result").get("action") == "Maths":
        result = req.get("result")
        parameters = result.get("parameters")
        n1 = parameters.get("number")
        n2 = parameters.get("number1")
        sign = parameters.get("cram-math")

        if sign == '+':
            res = int(n1) + int(n2)
        elif sign == '-':
            res = int(n1) - int(n2)
        elif sign == '/':
            if n2 != 0:
                res = int(n1) / int(n2)
            else:
                res = "Invalid"
        else:
            res = int(n1) * int(n2)

        print("Response: ")
        speech = "The " + sign + " of two values is: " + str(res)
        print(res)
        return {
            "speech": speech,
            "displayText": speech,
            "source": "Athena"
        }
    else:
        return {}


if __name__ == '__main__':
    port = int(os.getenv('POST', 80))
    print("Starting app on %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')
