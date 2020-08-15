import os
from sqlalchemy import Column, String, Integer, create_engine, Table, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

database_path = 'postgres://snkljcpdwalgvg:09268410a1f491cfeac7ec6150a5c7cafd10f11bceee4f751161aebe883d68d5@ec2-184-72-162-198.compute-1.amazonaws.com:5432/d1gh16kqs0coa8'

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
movie_actor_relationship_table = Table('movie_actor_relationship_table', db.Model.metadata,
                                       Column('movie_id', Integer, ForeignKey('movies.id')),
                                       Column('actor_id', Integer, ForeignKey('actors.id')))

'''
Movie

'''
class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String(80), unique=True, nullable=False)
  release_date = Column(Integer, nullable=False)

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
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  movies = db.relationship('Movie', secondary=movie_actor_relationship_table,
                             backref='movies_list', lazy=True)

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
