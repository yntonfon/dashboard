from flask_testing import TestCase

from app import bootstrap_app


class BaseTest(TestCase):
    def create_app(self):
        app = bootstrap_app(config='config.testing')
        self.db = app.extensions['sqlalchemy'].db
        self.mail = app.extensions['mail']
        
        return app
    
    def setUp(self):
        self.db.create_all()
    
    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
