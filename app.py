from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

import requests
import time

authKey = "e0bbaa859b5c43d3887e6cdbabbc2f74"

headers = {
    "authorization": authKey,
    "content-type": "application/json"
}

uploadURL = "https://api.assemblyai.com/v2/upload"
transcriptURL = "https://api.assemblyai.com/v2/transcript"


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r"*": {"origins": "*"}})


@app.route('/', methods=['GET', 'POST'])
def get_message():
    print("Got request in main function")
    return render_template("index.html")


@app.route('/upload_static_file', methods=['POST'])
def upload_static_file():
    print("Got request in static files")

    file = request.files['static_file']

    response = requests.post(
        uploadURL,
        headers=headers,
        data=file
    )

    json = response.json()

    resp = {"success": True, "response": "file saved!",
            "url": json["upload_url"]}
    return jsonify(resp), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(1521), debug=True)
