# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import json
from urlparse import urlparse

from gdata.service import RequestError
from douban.service import DoubanService
from diandou.settings import DOUBAN_API_KEY, DOUBAN_SECRET

client = DoubanService(api_key=DOUBAN_API_KEY, secret=DOUBAN_SECRET)

def _get_attribute(attributes, name):
    return [att.text for att in attributes
            if att.name == name]


def get_douban_movie(douban_id):
    uri = "/movie/subject/{0}".format(douban_id)

    try:
        return client.GetMovie(uri)
    except RequestError as e:
        err = json.loads(json.dumps(e.message))
        return None


def douban_search(text_query, start_index=0, max_results=10):
    feed = client.SearchMovie(text_query, start_index=start_index, max_results=max_results)
    movies = []
    for movie in feed.entry:
        movie_uri = urlparse(movie.id.text)
        douban_id = movie_uri.path.split('/')[-1:]
        movies.append(douban_id) #TODO: convert the douban entry to local format.

    return movies


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
