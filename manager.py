#-*- coding:utf-8 -*-
from flask.ext.script import Manager

from diandou import app
from diandou.models import db

manager = Manager(app)

@manager.command
def syncdb():
    db.create_all()

if __name__ == '__main__':
    manager.run()
