from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bailan@localhost:5432/redwinesdb'  # PostgreSQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class RedWine(db.Model):
    __tablename__ = 'red_wine_json'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    fixed_acidity = db.Column(db.Float, nullable=True)
    volatile_acidity = db.Column(db.Float, nullable=True)
    
# Create the database and the database table
with app.app_context():
    db.create_all()
