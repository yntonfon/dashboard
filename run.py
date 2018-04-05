from app import create_app
from app.model import db

app = create_app()
db.create_all(app=app)
app.run()
