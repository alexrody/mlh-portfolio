import unittest
import os
from peewee import *

from app import app, TimelinePost

os.environ['TESTING'] = 'true'

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class AppTestCase(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

        self.client = app.test_client()
    
    def tearDown(self):
        test_db.drop_tables([TimelinePost])
        test_db.close()
        
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        
        html = response.get_data(as_text=True)
        assert "<title>Álex Rody</title>" in html
        assert "<div id=\"profile-picture\" class=\"profile-picture\">" in html
        assert "<h2>About me</h2>" in html

    def test_timeline(self):
        # There are 0 posts initially:
        response_1 = self.client.get("/api/timeline_post")
        assert response_1.status_code == 200
        assert response_1.is_json
        
        json_1 = response_1.get_json()
        assert "timeline_posts" in json_1
        assert len(json_1["timeline_posts"]) == 0

        # Creating two unique posts:
        post_1 = self.client.post(
            '/api/timeline_post',
            data={
                'name': 'John Doe',
                'email': 'john@example.com',
                'content': "Hello world, I\'m John!"
            },
        )
        assert post_1.get_json()['id'] == 1

        post_2 = self.client.post(
            '/api/timeline_post',
            data={
                'name': 'Jane Doe',
                'email': 'jane@example.com',
                'content': "Hello world, I\'m Jane!"
            },
        )
        assert post_2.get_json()['id'] == 2

        # Checking that both posts exist on the timeline
        response_2 = self.client.get('/api/timeline_post')
        assert response_2.status_code == 200
        assert response_2.is_json

        json_after = response_2.get_json()
        assert "timeline_posts" in json_after
        assert len(json_after['timeline_posts']) == 2
        assert json_after['timeline_posts'][0]['name'] == 'Jane Doe'
        assert json_after['timeline_posts'][1]['name'] == 'John Doe'

        # Checking the timeline page itself
        response_3 = self.client.get('/timeline')
        assert response_3.status_code == 200
        
        html = response_3.get_data(as_text=True)
        print(html)
        assert "<div id=\"timeline\">" in html
        assert "<p>John Doe</p>" in html
        assert "<p>Jane Doe</p>" in html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            '/api/timeline_post',
            data={
                'name': "",
                'email': 'john@example.com',
                'content': "Hello world, I'm John!"
            },
        )
        assert response.status_code == 400
        
        html = response.get_data(as_text=True)
        assert "Invalid name" in html
        
        # POST request with empty content
        response = self.client.post(
            '/api/timeline_post',
            data={
                'name': 'John Doe',
                'email': 'john@example.com',
                'content': ""
            },
        )
        assert response.status_code == 400
        
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            '/api/timeline_post',
            data={
                'name': 'John Doe',
                'email': 'not-an-email',
                'content': "Hello world, I'm John!"
            },
        )
        assert response.status_code == 400
        
        html = response.get_data(as_text=True)
        assert "Invalid email" in html