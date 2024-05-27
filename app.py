#引入模块
from flask import Flask, render_template,request
import json
import requests
import db
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
