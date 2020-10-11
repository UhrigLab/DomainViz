from . import db

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.String(500))