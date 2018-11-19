import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    EMPLID = parameters.get("EMPLID")
    PARAMS = {'EMPLID':EMPLID}
    r=requests.get('http://oelser3.kovaion.com:8000/PSIGW/RESTListeningConnector/PSFT_HR/XX_EMPL_NAME.v1/?',json={"EMPLID": EMPLID})
    json_object = r.json()
    empl_name=json_object['XX_EMPL_NAME'][0]['XX_NAME']
    
    speech = "The EMPLOYEE name returned from Peoplesoft Database is:"+empl_name
    return {
    "speech": speech,
    "displayText": speech,
    "source": "Kovaion-Peoplesoft"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')

















