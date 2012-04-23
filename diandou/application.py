# -*- coding:utf-8 -*-
from flask import Flask, request, render_template
from flaskext.login import LoginManager

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

if __name__ == "__main__":
    app.run()
