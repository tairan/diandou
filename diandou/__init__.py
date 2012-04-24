# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from douban.service import DoubanService
from settings import DOUBAN_API_KEY, DOUBAN_SECRET

def _get_attribute(attributes, name):
    return [att.text for att in attributes
            if att.name == name]


def import_movie(mid):
    uri = "/movie/subject/{0}".format(mid)
    movie = {}
    svc = DoubanService(DOUBAN_API_KEY, DOUBAN_SECRET)
    d_movie = svc.GetMovie(uri)
    movie['id'] = d_movie.id.text
    movie['title'] = d_movie.title.text
    movie['aka'] = _get_attribute(d_movie.attribute, 'aka')
    #movie['category'] = [c.text for c in d_movie.category]
    movie['author'] = [a.name.text for a in d_movie.author]
    movie['cast'] = _get_attribute(d_movie.attribute, 'cast')
    #movie['content'] = d_movie.content
    #movie['contributor'] = d_movie.contributor
    #movie['control'] = d_movie.control
    movie['director'] = [att.text for att in d_movie.attribute if att.name == 'director']
    movie['link'] = [l.href for l in d_movie.link]
    movie['language'] = _get_attribute(d_movie.attribute, 'language')
    movie['image'] = [l.href for l in d_movie.link if l.rel == 'image'][0]
    #movie['published'] = d_movie.published
    movie['rating'] = d_movie.rating.average
    #movie['rights'] = d_movie.rights
    #movie['source'] = d_movie.source
    movie['summary'] = d_movie.summary.text
    movie['tag'] = [t.name for t in d_movie.tag]
    movie['type'] = _get_attribute(d_movie.attribute, 'movie_type')
    #movie['text'] = d_movie.text
    #movie['updated'] = d_movie.updated
    movie['writer'] = _get_attribute(d_movie.attribute, 'writer')
    movie['year'] = _get_attribute(d_movie.attribute, 'year')

    return movie

