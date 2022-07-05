#!/user/bin/env python3
# Authors: MLH, Javier Solis

import unittest
from peewee import *
from playhouse.shortcuts import model_to_dict

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:') # switching to an in-memory DB

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        
    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()
    
    def test_timeline_post(self):
        first_post = TimelinePost.create(
            name="John Doe",
            email="john@example.com",
            content="Hello world, I\'m John!"
        )
        assert first_post.id == 1

        second_post = TimelinePost.create(
            name="Jane Doe",
            email="Jane@example.com",
            content="Hello world, I\'m Jane!"
        )
        assert second_post.id == 2

        posts = [model_to_dict(post) for post in \
                TimelinePost.select().order_by(TimelinePost.id.asc())]
        assert posts[0]['id'] == 1
        assert posts[1]['id'] == 2