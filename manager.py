#-*- coding:utf-8 -*-
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
