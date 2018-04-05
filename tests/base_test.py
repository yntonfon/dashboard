from flask_testing import TestCase

from app import create_app
from app.model import db


class BaseTest(TestCase):
    def create_app(self):
        self.db = db
        return create_app('config.testing')
    
    def setUp(self):
        self.db.create_all()
    
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
