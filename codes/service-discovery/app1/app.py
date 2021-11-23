from flask import Flask
import os
import urllib.request
import json

app = Flask(__name__)
APP2_URL = "http://{}".format(os.getenv("APP2_URL"))


@app.route('/ping', methods=['GET'])
def healthcheck():
    return "ok"


@app.route('/', methods=['GET'])
def inc():
    data = {}
    app2_response = json.loads(urllib.request.urlopen(APP2_URL).read())
    data['app2_response'] = app2_response['response']
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
