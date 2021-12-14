from app import app
from flask_cors import CORS

CORS(app, origins="*")

app.run(host="0.0.0.0")
