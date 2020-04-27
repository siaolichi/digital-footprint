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

# # ssh2 Config
# from ssh2.session import Session
# rasp_host = '192.168.11.8'
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((rasp_host, 22))
# session = Session()
# session.handshake(sock)
# session.userauth_password('pi', '12345678')

for fi in pathlib.Path('./public/dist').iterdir():
    app.static('/' + fi.name, fi.resolve().as_posix())

def printHashCode(code):
  channel = session.open_session()
  channel.execute('sudo python3 /home/pi/python/printer.py "' + code + '"')
  channel.close()

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
@bp.route("/delete-photo", methods=['POST'])
async def index(request):
    code = request.json['code']
    os.remove("./public/dist/img/"+code+".jpg")
    print(code)
    return json({"message": "success"},
        headers={'X-Served-By': 'sanic'},
        status=200)
@bp.route("/delete-photo", methods=['OPTIONS'])
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