from flask import Flask, jsonify, render_template, request
from flask_cors import CORS


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

    print(request.files)
    f = request.files['static_file']
    f.save(f.filename)

    resp = {"success": True, "response": "file saved!"}
    return jsonify(resp), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(1521), debug=True)
