from cmath import exp
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)

exp = json.load(open("./app/static/json/experience.json"))
hob = json.load(open("./app/static/json/hobbies.json"))

@app.route('/')
def index():
    return render_template('index.html', title="Álex Rody", url=os.getenv("URL"))

@app.route('/experience')
def experience():
    return render_template('experience.jinja2', title="Álex Rody", experience=exp, url=os.getenv("URL"))

@app.route('/education')
def education():
    return "Education"

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.jinja2', title="Álex Rody", hobbies=hob, length=len(hob), url=os.getenv("URL"))