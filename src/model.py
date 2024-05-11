from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class log(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(20), nullable=False)



class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    short_description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)


class Attractions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    short_description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'