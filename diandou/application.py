# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from flaskext.login import LoginManager

from __init__ import import_movie

app = Flask(__name__)
app.config.from_object('settings')

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
    movie = import_movie(douban_id)
    return render_template('movie_details.html', movie=movie)


if __name__ == "__main__":
    app.run()
