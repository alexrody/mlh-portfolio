from cmath import exp
import datetime
import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from peewee import *
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=3306
)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(
        name=name,
        email=email,
        content=content
    )
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p) for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    id = request.form['id']
    mydb.execute(TimelinePost.delete().where(TimelinePost.id == id))
    return {'id': id}

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
