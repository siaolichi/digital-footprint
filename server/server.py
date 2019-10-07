from sanic import Blueprint, Sanic
from sanic.response import file, json
from sanic_cors import CORS, cross_origin
import pathlib
import os

import hashlib

# Environment Variable
from dotenv import load_dotenv
load_dotenv()
MONGODB_ADDR = os.getenv("MONGODB_ADDR")
PASSWORD = os.getenv("PASSWORD")
print(MONGODB_ADDR, PASSWORD)

app = Sanic(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

bp = Blueprint('blueprint', url_prefix='/')
# static_file_directory = os.path.join(os.path.dirname(__file__), 'static')

for fi in pathlib.Path('./public/dist').iterdir():
    app.static('/' + fi.name, fi.resolve().as_posix())

@bp.route("/hash-generator", methods=['POST'])
async def index(request):
    print(request.json)
    event_id = request.json['event_id']
    time = request.json['time']
    password = str(event_id) + " " + time + " " + PASSWORD
    photo_name = hashlib.sha224(str.encode( password )).hexdigest()
    print(event_id, time)
    return json({"result": photo_name},
        headers={'X-Served-By': 'sanic'},
        status=200)
@bp.route("/hash-generator", methods=['OPTIONS'])
async def index(request):
    return json({"message": "success"},
        headers={'X-Served-By': 'sanic'},
        status=200)

@bp.route('/', methods=["GET",])
async def index(request):
    return await file('public/dist/index.html')

app.blueprint(bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)