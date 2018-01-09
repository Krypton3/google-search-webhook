import json
import os

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


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
    elif req.get("result").get("action") == "Maths":
        result = req.get("result")
        parameters = result.get("parameters")
        n1 = parameters.get("number")
        n2 = parameters.get("number1")
        sign = parameters.get("cram-math")

        if sign == '+':
            res = int(n1) + int(n2)
        elif sign == '-':
            res = int(n1) + int(n2)
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
