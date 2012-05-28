# -*- coding:utf-8 -*-
import os

from flask import Flask, request, render_template, flash, redirect, url_for
from flaskext.login import LoginManager, login_required, login_user, logout_user

from diandou import app
from diandou.models import Movie, db, User
from diandou.utils import get_movie, douban_search

login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        current_user = User.query.filter_by(
            username=username, password=password).first()
        if current_user is None:
            return redirect(url_for('login'))
        else:
            login_user(current_user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for('dashboard'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def dashboard():
    return "<h1>Welcome admin</h1>"


@app.route('/')
def home():
    return redirect(url_for('movie_list'))


@app.route("/movie/<douban_id>")
def movie_details(douban_id):
    movie = Movie.query.filter_by(douban_id=douban_id).first()
    if movie is None:
        raise http_404

    return render_template('movie_details.html', movie=movie)


@app.route('/admin/movie/add/<douban_id>')
@login_required
def add_movie(douban_id):
    movie = get_movie(douban_id)
    if movie is None:
        return "404"

    exist = Movie.query.filter_by(douban_id=douban_id).first()
    if exist is None:
        movie = Movie(movie)
        db.session.add(movie)
        db.session.commit()

    return render_template('movie_details.html', movie=movie)


@app.route('/admin/movie/search')
def search_movies():
    key = request.args.get('q')
    if key is None:
        return redirect(url_for('search_movies'))
    result = Movie.query.filter(Movie.title.like(u"%{0}%".format(key))).all()
    if len(result) == 0:
        result = douban_search(key)

    return render_template('movie_list.html', movie_list=local_result)


@app.route('/test/search')
def search():
    key = request.args.get('q')
    result = douban_search(key)

    return render_template('test.html', keywords=key, result=result, result_attr=dir(result))


@app.route('/movie/list')
def movie_list():
    if request.args.get('type') != None:
        movie_list = Movie.query.filter(Movie.type.like(u"%{0}%".format(filter_type))).all()
    else:
        movie_list = Movie.query.all()

    return render_template('movie_list.html', movie_list=movie_list)


@app.route('/file')
def file_choice():
    if request.args.get('path') is None:
        return render_template('file.html', root_dirs=app.config['MEDIA_SERVER_PATH'])
    current_path = request.args.get('path')
    dirs = os.listdir(current_path)

    return render_template('file.html', dirs=dirs)
