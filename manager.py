#-*- coding:utf-8 -*-

try:
    from flask.ext.script import Manager
except ImportError:
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    activate_this = "{0}/env/bin/activate_this.py".format(current_dir)
    execfile(activate_this, dict(__file__=activate_this))
    from flask.ext.script import Manager

from diandou import app
from diandou.models import db, User
from diandou.tests import testing

manager = Manager(app)

@manager.command
def init():
    #db.drop_all()
    db.create_all()

@manager.command
def setup():
    admin = User('admin')
    admin.set_password("admin")
    db.session.add(admin)
    db.session.commit()

@manager.command
def test():
   testing()

if __name__ == '__main__':
    manager.run()
