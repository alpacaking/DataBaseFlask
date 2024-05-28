from flask import Flask
from models import db

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created!")
