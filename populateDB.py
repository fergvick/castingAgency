from models import db, Actor, Movie

# Actors Data

actor1 = Actor(
  name = "The Wild Sax Band",
  age = 23,
  gender = "Female"
)

actor2 = Actor(
  name = "The Wild Sax Band",
  age = 23,
  gender = "Female"
)

actor3 = Actor(
  name = "The Wild Sax Band",
  age = 23,
  gender = "Female"
)

# Movies Data

movie1 = Movie(
  title = "Godfather",
  release_date = 200320
)

movie2 = Movie(
  title = "Godfather",
  release_date = 200320
)

movie3 = Movie(
  title = "Godfather",
  release_date = 200320
)

db.session.add(actor1)
db.session.add(actor2)
db.session.add(actor3)
db.session.add(movie1)
db.session.add(movie2)
db.session.add(movie3)

db.session.commit()

