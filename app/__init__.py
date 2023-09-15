from flask import Flask
from config import Config

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config.from_object(Config)
app.secret_key = 'your_secret_key'

from app import routes
