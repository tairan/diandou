#-*- coding:utf-8 -*-
from flask.ext.script import Manager

from diandou import app

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
