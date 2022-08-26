from flask import Flask, request, make_response, jsonify
import markdown
import os
import boto3
import uuid
from datetime import datetime

app = Flask(__name__)
DYNAMODB_TABLE = os.getenv("<CHANGE_THIS_VAR>")

def save_data(markdown, html):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
    id = str(uuid.uuid4())
    table.update_item(
        Key={'ID': id},
        UpdateExpression="set message_markdown=:markdown, message_html=:html, request_date=:sts",
        ExpressionAttributeValues={
            ':markdown': markdown,
            ':html': html,
            ':sts': datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        })

@app.route('/ping', methods=['GET'])
def ping():
    try:
        return jsonify({"value": "ok"}), 200
    except:
        return jsonify({"error": "error"}), 500

@app.route('/api/markdown', methods=['GET', 'POST'])
def to_markdown():
    if request.method == "GET":
        data = {}
        return jsonify(data), 200
    elif request.method == "POST":
        payload = request.get_json()
        data = {}
        html = None
        if "text" in payload:
            input_markdown = payload['text']
            html = markdown.markdown(input_markdown)
            save_data(input_markdown, html)
            data["html"] = html
    return jsonify(data), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
