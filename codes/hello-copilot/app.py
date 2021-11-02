from flask import Flask, request, render_template
import platform
import psutil
import boto3
import socket

app = Flask(__name__, template_folder="./")

@app.route('/', methods=['GET'])
def hello():
    data = {}
    data['hostname'] = socket.gethostname()
    data['machine'] = platform.machine()
    data['system'] = platform.system()
    data['cpu_usage']=psutil.cpu_percent(interval=0)
    data['virtual_memory'] = psutil.virtual_memory().percent
    
    return render_template("index.html", data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
