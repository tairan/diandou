# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from flaskext.login import LoginManager

from diandou import app
from utils import import_movie

login_manager = LoginManager()
login_manager.setup_app(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        #TODO: login_user()
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("/admin"))

@app.route("/admin/movie/add")
def add_movie():
    raise NotImplemented

@app.route('/movie/<douban_id>')
def movie_details(douban_id):
    try:
        movie = import_movie(douban_id)
        from models import Movie, db
        if Movie.query.filter_by(douban_id=douban_id).first() is None:
            m = Movie(movie)
            db.session.add(m)
            db.session.commit()
    except BaseException as e:
        raise
        #return render_template('error.html', error=e)

    return render_template('movie_details.html', movie=movie)