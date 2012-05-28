# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from douban.service import DoubanService
from diandou.settings import DOUBAN_API_KEY


def _get_attribute(attributes, name):
    return [att.text for att in attributes
            if att.name == name]


def get_douban_movie(douban_id):
    uri = "/movie/subject/{0}".format(douban_id)
    client = DoubanService(api_key=DOUBAN_API_KEY)
    try:
        return client.GetMovie(uri)
    except BaseException:
        return None


def douban_search(query, start_index=0, max_result=10):
    #result = client.SearchMovie(query)
    result = client.QueryMovieByTag(query)
    #result = client.SearchPeople(query)

    return result


def get_movie(douban_id):
    douban_movie = get_douban_movie(douban_id)

    if douban_movie is None:
        return None
    
    movie = {}
    movie['id'] = douban_id
    movie['api_link'] = unicode(douban_movie.id.text)
    movie['title'] = unicode(douban_movie.title.text)
    movie['aka'] = _get_attribute(douban_movie.attribute, 'aka')
    movie['author'] = [a.name.text for a in douban_movie.author]
    movie['cast'] = _get_attribute(douban_movie.attribute, 'cast')
    movie['director'] = [att.text for att in douban_movie.attribute if att.name == 'director']
    movie['link'] = [l.href for l in douban_movie.link]
    movie['language'] = _get_attribute(douban_movie.attribute, 'language')
    movie['image'] = [l.href for l in douban_movie.link if l.rel == 'image'][0]
    movie['rating'] = douban_movie.rating.average
    movie['summary'] = unicode(douban_movie.summary.text)
    movie['tag'] = [t.name for t in douban_movie.tag]
    movie['type'] = _get_attribute(douban_movie.attribute, 'movie_type')
    movie['writer'] = _get_attribute(douban_movie.attribute, 'writer')
    movie['year'] = _get_attribute(douban_movie.attribute, 'year')

    return movie
