from . import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    surname=db.Column(db.String(50))
    numbers=relationship("PhoneNumber",cascade="all, delete-orphan")

class PhoneNumber(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    uid=db.Column(db.Integer, ForeignKey(User.id))
    phoneNumber=db.Column(db.String(50))
    type=db.Column(db.String(50))
    
