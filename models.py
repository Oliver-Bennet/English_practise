# models.py (mới)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    items = db.relationship('Item', backref='group', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sound = db.Column(db.String(10), nullable=False)
    words = db.Column(db.JSON, nullable=False)  # list words
    ipa = db.Column(db.String(20), nullable=False)
    guide = db.Column(db.String(200), nullable=False)
    approx = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.String(50), db.ForeignKey('group.id'), nullable=False)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False)
    ipa = db.Column(db.String(50), nullable=False)
    meaning = db.Column(db.String(200), nullable=False)