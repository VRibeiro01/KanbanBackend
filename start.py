from app import app
from flask_cors import CORS

CORS(app, origins=['127.0.0.1:8001'])

app.run(host="0.0.0.0")
