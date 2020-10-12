from . import db

class ImageFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    filepath = db.Column(db.String(500))