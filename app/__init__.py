from cmath import exp
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

exp = json.load(open("./app/static/json/experience.json"))
edu = json.load(open("./app/static/json/education.json"))
hob = json.load(open("./app/static/json/hobbies.json"))
loc = json.load(open("./app/static/json/locations.json"))

@app.route('/')
def index():
    return render_template('index.html', title="Álex Rody", url=os.getenv("URL"))

@app.route('/experience')
def experience():
    return render_template('experience.jinja2', title="Álex Rody", section="Experience", experience=exp, url=os.getenv("URL"))

@app.route('/education')
def education():
    return render_template('experience.jinja2', title="Álex Rody", section="Education", experience=edu, url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.jinja2', title="Álex Rody", hobbies=hob, length=len(hob), url=os.getenv("URL"))

@app.route('/map')
def map():
    return render_template('map.jinja2', title="Álex Rody", locations=loc, url=os.getenv("URL"))
