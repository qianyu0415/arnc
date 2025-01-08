from arnc import db
import pytz
from datetime import datetime

class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False, unique = True)
    email = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(20), nullable = False)
    videos = db.relationship("Video", backref = "account")
    bgs = db.relationship("Bg", backref = "account")
    masks = db.relationship("Mask", backref = "account")


class Video(db.Model):
    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Enum('3D', 'ma'), nullable = True)
    name = db.Column(db.String(100), unique = True)
    date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')))
    dir = db.Column(db.String(100), nullable = False, unique = True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))


class Bg(db.Model):
    __tablename__ = "bg"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')))
    dir = db.Column(db.String(100), nullable = False, unique = True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    masks = db.relationship("Mask", backref = "bg")
 

class Mask(db.Model):
    __tablename__ = "mask"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique = True)
    date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')))
    dir = db.Column(db.String(100), nullable = False, unique = True)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    bg_id = db.Column(db.Integer, db.ForeignKey("bg.id"))
    
