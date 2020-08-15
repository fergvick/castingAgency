import os
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

database_path = 'postgres://swxayeqfonggry:338e4eb17b6dd460381b43cbfa8a38c0069fb2859a6f84f59c2cdb8e0e193fc7@ec2-34-204-22-76.compute-1.amazonaws.com:5432/d8qvbansrhno7g'
# database_path = 'sqlite:///'

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

'''
Many to many between movies and actors

'''
movie_actor_relationship_table = db.Table('movie_actor_relationship_table',
  db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'), primary_key=True),
  db.Column('actor_id', db.Integer, db.ForeignKey('Actor.id'), primary_key=True)
)

'''
Movie

'''
class Movie(db.Model):  
  __tablename__ = 'Movie'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(80), unique=True, nullable=False)
  release_date = db.Column(db.Integer, nullable=False)

  def __init__(self, title, release_date):
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'release_date': self.release_date
    }

'''
Actor

'''
class Actor(db.Model):  
  __tablename__ = 'Actor'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))
  age = db.Column(db.Integer)
  gender = db.Column(db.String)
  movies = db.relationship('Movie', secondary=movie_actor_relationship_table, backref=db.backref('venues', lazy=True))

  def __init__(self, name, age, gender):
    self.name = name
    self.age = age
    self.gender = gender

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
    }
