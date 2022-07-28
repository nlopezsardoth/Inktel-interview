from flask import Flask, jsonify, render_template, request, json
from flask_cors import CORS

import logging
import requests
import time
import re

logging.basicConfig(filename="logFile.log", level=logging.INFO,
                    format="%(asctime)s:%(name)s:%(message)s")

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
    logging.info(f"Main")
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['static_file']

    response = requests.post(
        uploadURL,
        headers=headers,
        data=file
    )

    json = response.json()

    url = json["upload_url"]

    logging.info(f"Upload: {url}")

    resp = {"success": True, "response": "file saved!",
            "url": url}
    return jsonify(resp), 200


@app.route('/transcribe', methods=['POST'])
def transcribe():

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
        logging.info(f"Transcribe: Error")
        resp = {"success": False,
                "response": "Error occurred when trying to transcribe the file"}
        return jsonify(resp), 400

    else:
        logging.info(f"Transcribe: {transcriptionID}")

        resp = {"success": True, "response": "file transcribed!",
                "id": transcriptionID}
        return jsonify(resp), 200


@app.route('/search', methods=['POST'])
def search():

    data = json.loads(request.data.decode())
    transcriptionId = data["id"]
    text = data["search"]

    text = re.sub(r'[^\w\s]', '', text)
    text = text.split()
    words = (",".join(sorted(set(text), key=text.index)))

    response = requests.get(
        f"{transcriptURL}/{transcriptionId}/word-search?words={words}",
        headers=headers,
    )

    jResponse = response.json()
    matches = jResponse["matches"]

    if not matches:
        logging.info(f"Search: No match")
        resp = {"success": True,
                "response": "No match found"}
        return jsonify(resp), 204
    else:
        for match in matches:
            timestamps = []
            match.pop("indexes")
            for time in match["timestamps"]:
                timestamps.append(time[0]/1000)
            match["timestamps"] = ", ".join(str(stamp) for stamp in timestamps)

        logging.info(f"Search: {matches}")

        resp = {"success": True, "response": "file saved!",
                "match": matches}
        return jsonify(resp), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(1521), debug=True)
