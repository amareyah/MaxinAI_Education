import json
import datetime
from flask import Flask
from pathlib import Path

app = Flask(__name__)
BASE_FOLDER = Path(__file__).parent
RESOURCE_FILE = BASE_FOLDER/"resources"/"resource.json"


@app.route('/', methods=['GET'])
def index():
    return {"message": "connection is OK"}, 200


@app.route('/hello', methods=["GET"])
def hello_you():
    with open(RESOURCE_FILE) as f:
        file_content = f.read()
        json_cont = json.loads(file_content)
        content = json_cont.get('welcome to maxinai')
        date_str = datetime.datetime.now().strftime("%d %b %Y - %H:%M:%S")
        result = f'{content} - {date_str}'
        if result:
            return result, 200

    return {"message": "Huston, we have a problem"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
