import unittest

from flask import Flask, current_app

from app import create_app, Base
from app.config import TestConfig
from models.userprofile import UserProfile
from scripts.initial_script import initial_fill


class GroupResourseCase(unittest.TestCase):
    def setUp(self):
        self.application = create_app(config_class=TestConfig)
        Base.metadata.create_all(bind=self.application.engine)
        initial_fill(self.application)
        self.app = self.application.test_client()


    def tearDown(self):
        Base.metadata.drop_all()

    def test_get_by_id(self):
        resp = self.app.get('/group/1')
        x = self.application.session.query(UserProfile).all()
        self.assertEqual(resp.json['name'], 'Latexfauna')


if __name__ == '__main__':
    unittest.main()
