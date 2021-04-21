# Import Flask / Had to create a new env and add Flask to the project
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world'
