# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from douban.service import DoubanService
from diandou.settings import DOUBAN_API_KEY, DOUBAN_SECRET

def _get_attribute(attributes, name):
    return [att.text for att in attributes
            if att.name == name]


def import_movie(mid):
    uri = "/movie/subject/{0}".format(mid)
    movie = {}
    svc = DoubanService(DOUBAN_API_KEY, DOUBAN_SECRET)

    try:
        d_movie = svc.GetMovie(uri)
    except BaseException:
        raise

    movie['id'] = mid
    movie['api_link'] = unicode(d_movie.id.text)
    movie['title'] = unicode(d_movie.title.text)
    movie['aka'] = _get_attribute(d_movie.attribute, 'aka')
    movie['author'] = [a.name.text for a in d_movie.author]
    movie['cast'] = _get_attribute(d_movie.attribute, 'cast')
    movie['director'] = [att.text for att in d_movie.attribute if att.name == 'director']
    movie['link'] = [l.href for l in d_movie.link]
    movie['language'] = _get_attribute(d_movie.attribute, 'language')
    movie['image'] = [l.href for l in d_movie.link if l.rel == 'image'][0]
    movie['rating'] = d_movie.rating.average
    movie['summary'] = unicode(d_movie.summary.text)
    movie['tag'] = [t.name for t in d_movie.tag]
    movie['type'] = _get_attribute(d_movie.attribute, 'movie_type')
    movie['writer'] = _get_attribute(d_movie.attribute, 'writer')
    movie['year'] = _get_attribute(d_movie.attribute, 'year')

    return movie

