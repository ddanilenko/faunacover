import unittest

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import application
from app.database import Base
from app.models.group import Group


class GroupResourseCase(unittest.TestCase):
    def setUp(self):
        application = Flask(__name__)
        application.config.from_object(Config)
        self.app = application.test_client()
        application.config['TESTING'] = True


    # def tearDown(self):
    #     Base.metadata.drop_all()

    def test_get_by_id(self):
        resp = self.app.get('/group/1')
        self.assertEqual(resp.json['name'], 'Latexfauna')


if __name__ == '__main__':
    unittest.main()
