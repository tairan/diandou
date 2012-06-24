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

    m1 = Media(1, 'a.avi', 'xxj', 'aka')
    m2 = Media(2, 'b.rmvb', 'xxx', 'aka')
    db.session.add(m1)
    db.session.add(m2)
    db.session.commit()

    f1 = MovieFile(movie, m1)
    f2 = MovieFile(movie, m2)
    db.session.add(f1)
    db.session.add(f2)
    db.session.commit()

