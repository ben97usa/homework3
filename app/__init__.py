# __init__.py
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()

app = Flask(__name__, template_folder='../templates')
CORS(app)

print(app.template_folder)

# Access environment variables
app.config['TIINGO_API_TOKEN'] = os.getenv('TIINGO_API_TOKEN')

from app import routes