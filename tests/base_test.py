from flask_testing import TestCase

from app import create_app


class BaseTest(TestCase):
    def create_app(self):
        app = create_app('config.testing')
        self.db = app.extensions['sqlalchemy'].db
        self.mail = app.extensions['mail']
        
        return app
    
    def setUp(self):
        self.db.create_all()
    
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
