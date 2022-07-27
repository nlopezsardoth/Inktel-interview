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


@app.route('/upload', methods=['POST'])
def upload():
    print("Got upload request")

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


@app.route('/transcribe', methods=['POST'])
def transcribe():
    print("Got transcribing request")

    audioID = request.data.decode("utf-8")

    def _startTranscription(aURL):
        response = requests.post(
            transcriptURL,
            headers=headers,
            json={"audio_url": aURL}
        )

        json = response.json()

        return json["id"]

    transcriptionID = _startTranscription(audioID)

    maxAttempts = 10
    timedout = False

    while True:
        response = requests.get(
            f"{transcriptURL}/{transcriptionID}",
            headers=headers,
        )

        json = response.json()

        if json["status"] == "completed":
            break

        maxAttempts -= 1
        timedout = maxAttempts <= 0

        if timedout:
            break

        # Waiting 3 seconds before next try
        time.sleep(3)

    if timedout:
        resp = {"success": False,
                "response": "Error occurred when trying to transcribe the file"}
        return jsonify(resp), 400

    else:
        resp = {"success": True, "response": "file transcribed!",
                "id": transcriptionID}
        return jsonify(resp), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(1521), debug=True)
