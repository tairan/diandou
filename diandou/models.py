# -*- coding:utf-8 -*-
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery
from flask.ext.login import UserMixin

from diandou import app
db = SQLAlchemy(app)
from diandou.mediatomb import *


class MovieQuery(BaseQuery):

    def get_by_douban_id(self, douban_id):
        return self.filter(Movie.douban_id==douban_id).first()

    def get_files(self, douban_id):
        movie = Movie.query.filter(Movie.douban_id==douban_id).first()
        return movie, sorted(MovieFile.query.filter(MovieFile.movie_id==movie.id).all())

    def to_list(self, tag=None):
        if not tag is None:
            movie_list = self.filter(Movie.type.like(u"%{0}%".format(tag))).order_by(Movie.year.desc())
        else:
            movie_list = self.order_by(Movie.year.desc())
        return movie_list.all()


class Movie(db.Model):

    query_class = MovieQuery

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

    def __init__(self, movie, media):
        self.movie_id = movie.id
        self.media_id = media.id

    id = db.Column(db.Integer, primary_key=True)

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    movie = db.relationship('Movie',
                            backref=db.backref('items', lazy='dynamic'))

    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    media = db.relationship('Media',
                            backref=db.backref('files', lazy='dynamic'))



class UserQuery(BaseQuery):

    def authenticate(self, username, password):
        user = self.filter(User.username==username).filter(User.password==password).first()
        return user


class User(db.Model, UserMixin):

    query_class = UserQuery

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(128))

    def __init__(self, username):
        self.username = username
        self.password = None

    def __unicode__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = raw_password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
