import unittest
import os
from flask import json
from playhouse.shortcuts import model_to_dict
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        
        html = response.get_data(as_text=True)
        assert "<title>Álex Rody</title>" in html
        assert "<div id=\"profile-picture\" class=\"profile-picture\">" in html
        assert "<h2>About me</h2>" in html

    def test_timeline(self):
        response_before = self.client.get('/api/timeline_post')
        assert response_before.status_code == 200
        assert response_before.is_json
        json_before = response_before.get_json()
        assert "timeline_posts" in json_before
        assert len(json_before['timeline_posts']) == 0
        # Create 2 posts
        post_1 = self.client.post(
            '/api/timeline_post',
            data={
                'name': 'John Doe',
                'email': 'john@example.com',
                'content': "Hello world, I'm John!"
            },
        )

        assert post_1.status_code == 200

        # Creating another post:
        post_2 = self.client.post(
            '/api/timeline_post',
            data={
                'name': 'Jane Doe',
                'email': 'jane@example.com',
                'content': "Hello world, I\'m Jane!",
            },
        )
        assert post_2.status_code == 200

        # Checking that both posts exist on the timeline
        response_3 = self.client.get('/api/timeline_post')
        assert response_3.status_code == 200
        assert response_3.is_json

        json_3 = response_3.get_json()
        assert "timeline_posts" in json_3
        # assert len(json_3['timeline_posts']) == 2
        assert json_3['timeline_posts'][0]['name'] == 'Jane Doe'
        assert json_3['timeline_posts'][1]['name'] == 'John Doe'

        # Checking the timeline page itself
        response_4 = self.client.get('/timeline')
        assert response_4.status_code == 200
        
        html = response_4.get_data(as_text=True)
        assert "<div id=\"timeline\">" in html

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