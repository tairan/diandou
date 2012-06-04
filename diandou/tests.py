# -*- coding:utf-8 -*-

from diandou.models import *
from diandou.utils import *

def testing():
    douban = ['4739952', '4036000', '5244092']
    for m in douban:
        dm = get_movie(m)
        m = Movie(dm)
        db.session.add(m)
        db.session.commit()
    movie = Movie.query.filter(Movie.douban_id=='4739952').first()
    f1 = MovieFile(movie, 'http://media.tairan.org/file/1')
    f2 = MovieFile(movie, 'http://media.tairan.org/file/2')
    db.session.add(f1)
    db.session.add(f2)
    db.session.commit()

