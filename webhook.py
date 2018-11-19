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
    
    res = processRequest(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    EMPLID = parameters.get("EMPLID")
    PARAMS = {'EMPLID':EMPLID}
     if EMPLID is None:
        return None
    r=requests.get('http://oelser3.kovaion.com:8000/PSIGW/RESTListeningConnector/PSFT_HR/XX_EMPL_NAME.v1/?',emplid=PARAMS)
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
    app.run(debug=False, port=port, host='0.0.0.0')

















