import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# get database url from environment
database_name = "casting"
database_path = "postgres://{}:{}@{}/{}".format('sara', 'sara','localhost:5432', database_name)
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()


'''
Movie
'''


class Movie(db.Model):
    __tablename__ = 'movies'
    movie_id = Column(Integer, primary_key=True)
    movie_title = Column(String(120), unique=True, nullable=False)
    movie_release_date = Column(DateTime(), nullable=False)

    def __init__(self, movie_title, movie_release_date):
        self.movie_title = movie_title
        self.movie_release_date = movie_release_date

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
            'movie_id': self.movie_id,
            'movie_title': self.movie_title,
            'movie_release_date': self.movie_release_date
        }


'''
Actor
'''


class Actor(db.Model):
    __tablename__ = 'actors'

    actor_id = Column(Integer, primary_key=True)
    actor_name = Column(String, nullable=False)
    actor_age = Column(Integer, nullable=False)
    actor_gender = Column(String, nullable=False)

    def __init__(self, actor_id, actor_name, actor_age, actor_gender):
        self.actor_id = actor_id
        self.actor_name = actor_name
        self.actor_age = actor_age
        self.actor_gender = actor_gender

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
            'actor_id': self.actor_id,
            'actor_name': self.actor_name,
            'actor_age': self.actor_age,
            'actor_gender': self.actor_gender
        }
