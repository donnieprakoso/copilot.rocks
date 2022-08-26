from flask import Flask, request, render_template
import platform
import psutil
import boto3
import socket
import os
import logging

# from flask import jsonify
# import json
# from urllib import request, parse

app = Flask(__name__, template_folder="./")

@app.route('/ping', methods=['GET'])
def ping():
    try:
        return jsonify({"value": "ok"}), 200
    except:
        return jsonify({"error": "error"}), 500

@app.route('/web', methods=['GET'])
def hello():
    data = {}
    data['hostname'] = socket.gethostname()
    data['machine'] = platform.machine()
    data['system'] = platform.system()
    data['cpu_usage']=psutil.cpu_percent(interval=0)
    data['virtual_memory'] = psutil.virtual_memory().percent

    return render_template("index.html", data=data)

# @app.route('/web/markdown', methods=['GET'])
# def get_markdown():
    # payload = {"text":"Calling from the web"}
    # req =  request.Request(os.getenv("LOCAL_SVCAPI_URL"), data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    # resp = request.urlopen(req)
    # resp_json = json.loads(resp.read())
    # return jsonify(resp_json), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
