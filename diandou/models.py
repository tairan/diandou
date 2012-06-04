#-*- coding:utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin

from diandou import app

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    douban_id = db.Column(db.String(8), unique=True)
    api_link = db.Column(db.String(256), unique=True)
    title = db.Column(db.String(128))
    aka = db.Column(db.String(1024))
    cast = db.Column(db.String(1024))
    director = db.Column(db.String(1024))
    link = db.Column(db.String(1024))
    language = db.Column(db.String(1024))
    image = db.Column(db.String(1024))
    rating = db.Column(db.Integer)
    summary = db.Column(db.String(5120))
    tag = db.Column(db.String(1024))
    type = db.Column(db.String(1024))
    writer = db.Column(db.String(1024))
    year = db.Column(db.String(4))

    def __init__(self, movie):
        self.douban_id = movie['id']
        self.api_link = movie['api_link']
        self.title = movie['title']
        self.aka = u','.join(movie['aka'])
        self.cast = u','.join(movie['cast'])
        self.director = u','.join(movie['director'])
        self.link = u','.join(movie['link'])
        self.language = u','.join(movie['language'])
        self.image = movie['image']
        self.rating = movie['rating']
        self.summary = movie['summary']
        self.tag = u','.join(movie['tag'])
        self.type = u','.join(movie['type'])
        self.writer = u','.join(movie['writer'])
        self.year = movie['year'][0]


class MovieFile(db.Model):
    
    def __init__(self, movie, path):
        self.movie = movie
        self.path  = path

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(512))

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    movie = db.relationship('Movie',
                            backref=db.backref('items', lazy='dynamic'))


def find_movie_files(douban_id):
    movie = Movie.query.filter(Movie.douban_id == douban_id).first()
    files = []
    if not movie is None:
        files = MovieFile.query.filter(MovieFile.movie_id == movie.id).all()
    return files


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(128))
    
    def __init__(self, username):
        self.username = username
        self.password = None

    def set_password(self, raw_password):
        self.password = raw_password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
