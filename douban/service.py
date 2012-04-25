# encoding: UTF-8

import atom
import gdata
import gdata.service
import douban
import urllib
import oauth, client

class DoubanService(gdata.service.GDataService):
    def __init__(self, api_key=None, secret=None,
            source='douban-python', server='api.douban.com', 
            additional_headers=None):
        self.api_key = api_key
        self.client = client.OAuthClient(key=api_key, secret=secret)
        gdata.service.GDataService.__init__(self, service='douban', source=source,
                server=server, additional_headers=additional_headers)

    def GetAuthorizationURL(self, key, secret, callback=None):
        return self.client.get_authorization_url(key, secret, callback)

    def ProgrammaticLogin(self, token_key=None, token_secret=None):
        return self.client.login(token_key, token_secret)

    def Get(self, uri, extra_headers={}, *args, **kwargs):
        auth_header = self.client.get_auth_header('GET', uri)
        if auth_header:
            extra_headers.update(auth_header)
        elif self.api_key:
            param = urllib.urlencode([('apikey', self.api_key)])
            if '?' in uri:
                uri += '&' + param
            else:
                uri += '?' + param
        return gdata.service.GDataService.Get(self, uri, extra_headers, *args, **kwargs)        
    def Post(self, data, uri, extra_headers=None, url_params=None, *args, **kwargs):
        if extra_headers is None:
            extra_headers = {}
        extra_headers.update(self.client.get_auth_header('POST', uri, url_params))
        return gdata.service.GDataService.Post(self, data, uri, 
                extra_headers, url_params, *args, **kwargs)
    
    def Put(self, data, uri, extra_headers=None, url_params=None, *args, **kwargs):
        if extra_headers is None:
            extra_headers = {}
        extra_headers.update(self.client.get_auth_header('PUT', uri, url_params))
        return gdata.service.GDataService.Put(self, data, uri, 
                extra_headers, url_params, *args, **kwargs)

    def Delete(self, uri, extra_headers=None, url_params=None, *args, **kwargs):
        if extra_headers is None:
            extra_headers = {}
        extra_headers.update(self.client.get_auth_header('DELETE', uri, url_params))
        return gdata.service.GDataService.Delete(self, 
        uri, extra_headers, url_params, *args, **kwargs)

    def GetPeople(self, uri):
        return self.Get(uri, converter=douban.PeopleEntryFromString)

    def GetPeopleFeed(self, uri):
        return self.Get(uri, converter=douban.PeopleFeedFromString)

    def SearchPeople(self, text_query, start_index=None, max_results=None):
        query = Query('/people/', text_query, start_index=start_index,
                max_results=max_results)
        return self.GetPeopleFeed(query.ToUri())
    
    def GetFriends(self, uri):
        return self.Get(uri, converter=douban.PeopleFeedFromString)

    def GetContacts(self, uri):
        return self.Get(uri, converter=douban.PeopleFeedFromString)

    def GetAuthorizedUID(self, uri):
        return self.Get(urllib.quote(uri), converter=douban.PeopleEntryFromString)

    def GetBook(self, uri):
        return self.Get(uri, converter=douban.BookEntryFromString)

    def GetBookFeed(self, uri):
        return self.Get(uri, converter=douban.BookFeedFromString)

    def SearchBook(self, text_query, start_index=None, max_results=None):
        query = Query('/book/subjects', text_query=text_query,
                start_index=start_index, max_results=max_results)
        return self.GetBookFeed(query.ToUri())

    def QueryBookByTag(self, tag, start_index=None, max_results=None):
        query = Query('/book/subjects', text_query=None,
                start_index=start_index, max_results=max_results, tag=tag)
        return self.GetBookFeed(query.ToUri())

    def GetMovie(self, uri):
        return self.Get(uri, converter=douban.MovieEntryFromString)

    def GetMovieFeed(self, uri):
        return self.Get(uri, converter=douban.MovieFeedFromString)

    def SearchMovie(self, text_query, start_index=None, max_results=None):
        query = Query('/movie/subjects', text_query=text_query,
                start_index=start_index, max_results=max_results)
        return self.GetMovieFeed(query.ToUri())

    def QueryMovieByTag(self, tag, start_index=None, max_results=None):
        query = Query('/movie/subjects', text_query=None,
                start_index=start_index, max_results=max_results, tag=tag)
        return self.GetMovieFeed(query.ToUri())

    def GetMusic(self, uri):
        return self.Get(uri, converter=douban.MusicEntryFromString)

    def GetMusicFeed(self, uri):
        return self.Get(uri, converter=douban.MusicFeedFromString)

    def SearchMusic(self, text_query, start_index=None, max_results=None):
        query = Query('/music/subjects', text_query=text_query,
                start_index=start_index, max_results=max_results)
        return self.GetMusicFeed(query.ToUri())

    def QueryMusicByTag(self, tag, start_index=None, max_results=None):
        query = Query('/music/subjects', text_query=None,
                start_index=start_index, max_results=max_results, tag=tag)
        return self.GetMusicFeed(query.ToUri())

    def GetReview(self, uri):
        return self.Get(uri, converter=douban.ReviewEntryFromString)

    def GetReviewFeed(self, uri, orderby = 'score'):
        query = Query(uri, text_query=None, start_index=None, max_results=None, orderby=orderby)
        return self.Get(query.ToUri(), converter=douban.ReviewFeedFromString)

    def CreateReview(self, title, content, subject, rating=None):
        subject = douban.Subject(atom_id=subject.id)
        entry = douban.ReviewEntry(subject=subject)
        if rating:
            entry.rating = douban.Rating(value=rating)
        entry.title = atom.Title(text=title)
        entry.content = atom.Content(text=content)
        return self.Post(entry, '/reviews', 
                converter=douban.ReviewEntryFromString)
        
    def UpdateReview(self, entry, title, content, rating=None):
        if isinstance(entry,(str,unicode)):
            entry = self.Get(entry, douban.ReviewEntryFromString)
            
        entry.title = atom.Title(text=title)
        entry.content = atom.Content(text=content)
        if rating:
             entry.rating = douban.Rating(value=rating)
        
        uri = entry.GetSelfLink().href  
        return self.Put(entry, uri, converter=douban.ReviewEntryFromString)
        
    def DeleteReview(self, entry):
        uri = entry.GetSelfLink().href  
        return self.Delete(uri)
        
    def GetCollection(self, uri):
        return self.Get(uri, converter=douban.CollectionEntryFromString)
        
    def GetCollectionFeed(self, uri):
        return self.Get(uri, converter=douban.CollectionFeedFromString)

   # def GetMyCollection(self):
   #     return self.Get(urllib.quote('/people/@me/collection'), 
   #         converter=douban.CollectionFeedFromString)
    def GetMyCollection(self, url, cat=None, tag=None, status=None, start_index=None, 
        max_results=None, updated_max=None, updated_min=None):
        if updated_max and updated_min and status:
            query = Query(url, text_query=None, start_index=start_index, 
                max_results=max_results, status=status, tag=tag, cat=cat, 
                updated_max=updated_max, updated_min=updated_min)
        elif status:
            query = Query(url, text_query=None, start_index=start_index, 
                max_results=max_results, tag=tag, cat=cat, status=status)
        elif updated_max and updated_min:
            query = Query(url, text_query=None, start_index=start_index, 
                max_results=max_results, tag=tag, cat=cat, 
                updated_max=updated_max, updated_min=updated_min)
        else:
            query = Query(url, text_query=None, start_index=start_index, 
                max_results=max_results, tag=tag, cat=cat)
        return self.GetCollectionFeed(query.ToUri())
    
    def AddCollection(self, status, subject, rating=None, tag=[], private=True):
        subject = douban.Subject(atom_id=subject.id)
        entry = douban.CollectionEntry(subject=subject,
                status=douban.Status(status))
        if rating:
            entry.rating = douban.Rating(rating)
        if isinstance(tag, (str,unicode)):
            tag = filter(None, tag.split(' '))
        if private:
            attribute = douban.Attribute('privacy', 'private')
            entry.attribute.append(attribute)
        else:
            attribute = douban.Attribute('privacy', 'public')
            entry.attribute.append(attribute)
        entry.tags = [douban.Tag(name=t) for t in tag]
        return self.Post(entry, '/collection', 
                converter=douban.CollectionEntryFromString)

    def UpdateCollection(self, entry, status, tag=[], rating=None, private=False):
        if isinstance(entry,(str,unicode)):
            entry = self.Get(entry, douban.CollectionEntryFromString)
        
        entry.status = douban.Status(status)
        if rating:
             entry.rating = douban.Rating(rating)
        if tag:
            if isinstance(tag, (str,unicode)):
                tag = filter(None, tag.split(' '))
            entry.tags = [douban.Tag(name=t) for t in tag]
        else:
            entry.tags = [douban.Tag(name=t.name) for t in entry.tags]
        if private:
            attribute = douban.Attribute('privacy', 'private')
            entry.attribute.append(attribute)
        else:
            attribute = douban.Attribute('privacy', 'public')
            entry.attribute.append(attribute)
        uri = entry.GetSelfLink().href  
        return self.Put(entry, uri, converter=douban.CollectionEntryFromString)
    
    def DeleteCollection(self, entry):
        uri = entry.GetSelfLink().href  
        return self.Delete(uri)

    def GetTagFeed(self, uri):
        return self.Get(uri, converter=douban.TagFeedFromString)
  
    def GetBroadcastingFeed(self, uri, start_index=None, max_results=None):
        query = Query(uri, text_query=None, 
        start_index=start_index, max_results=max_results)
        return self.Get(query.ToUri(), converter=douban.BroadcastingFeedFromString)
    
    def GetContactsBroadcastingFeed(self, uri, start_index=None, max_results=None):
        query = Query(uri, text_query=None, 
        start_index=start_index, max_results=max_results)
        return self.Get(query.ToUri(), converter=douban.BroadcastingFeedFromString)

    def AddBroadcasting(self, uri, entry):
        return self.Post(entry, uri, converter=douban.BroadcastingEntryFromString)

    def DeleteBroadcasting(self, entry):
        uri = entry.id.text
        return self.Delete(uri)
   
    def GetNote(self, uri):
        return self.Get(uri, converter=douban.NoteEntryFromString)
 
    def GetMyNotes(self, uri, start_index=None, max_results=None):
        query = Query(uri, text_query=None, 
        start_index=start_index, max_results=max_results)
        return self.Get(query.ToUri(), converter=douban.NoteFeedFromString)

    def AddNote(self, uri, entry, private=False, can_reply=True):
        if private:
            attribute = douban.Attribute('privacy', 'private')
            entry.attribute.append(attribute)
        else:
            attribute = douban.Attribute('privacy', 'public')
            entry.attribute.append(attribute)
        if can_reply:
            attribute = douban.Attribute('can_reply', 'yes')
            entry.attribute.append(attribute)
        else:
            attribute = douban.Attribute('can_reply', 'no')
            entry.attribute.append(attribute)
        return self.Post(entry, uri, converter=douban.NoteEntryFromString)

    def UpdateNote(self, entry, content, title, private=True, can_reply=True):
        if isinstance(entry,(str,unicode)):
            entry = self.Get(entry, douban.NoteEntryFromString)
            
        entry.title = atom.Title(text=title)
        entry.content = atom.Content(text=content)
        if private:
            attribute = douban.Attribute('privacy', 'private')
            entry.attribute.append(attribute)
        else:
            attribute = douban.Attribute('privacy', 'public')
            entry.attribute.append(attribute)
        if can_reply:
            attribute = douban.Attribute('can_reply', 'yes')
            entry.attribute.append(attribute)
        else:
            attribute = douban.Attribute('can_reply', 'no')
            entry.attribute.append(attribute)
        uri = entry.id.text
        return self.Put(entry, uri, converter=douban.NoteEntryFromString)

    def DeleteNote(self, entry):
        uri = entry.id.text
        return self.Delete(uri)

    def GetEvent(self, uri):
        return self.Get(uri, converter=douban.EventEntryFromString)

    def GetEventFeed(self, uri):
        return self.Get(uri, converter=douban.EventFeedFromString)

    def SearchEvent(self, text_query, location, start_index=None, max_results=None):
        query = Query('/events', text_query, location=location, start_index=start_index,
                max_results=max_results)
        return self.GetEventFeed(query.ToUri())

    def GetLocationEvents(self, location, type=None, start_index=None, max_results=None):
        query = Query('/event/location/%s' %location, type=type or 'all', start_index=start_index, max_results=max_results)
        return self.GetEventFeed(query.ToUri())
 
    def GetEvents(self, uri, start_index=None, max_results=None, status=None):
        query = Query('%s%s' %(uri, status and '/%s' %status or ''), start_index=start_index, max_results=max_results)
        return self.Get(query.ToUri(), converter=douban.EventFeedFromString)

    def GetEventWishers(self, uri, start_index=None, max_results=None):
        query = Query('%s/wishers'%uri, start_index=start_index, max_results=max_results)
        return self.Get(query.ToUri(), converter=douban.PeopleFeedFromString)

    def GetEventParticipants(self, uri, start_index=None, max_results=None):
        query = Query('%s/participants'%uri, start_index=start_index, max_results=max_results)
        return self.Get(query.ToUri(), converter=douban.PeopleFeedFromString)

    def DeleteEventWisher(self, uri):
        return self.Delete('%s/wishers' %uri)
        
    def DeleteEventParticipants(self, uri):
        return self.Delete('%s/participants' %uri)
 
    def AddEvent(self, uri, entry, invite_only=False, can_invite=True):
        entry.attribute.append(douban.Attribute('invite_only', invite_only and 'yes' or 'no'))
        entry.attribute.append(douban.Attribute('can_invite', can_invite and 'yes' or 'no'))
        return self.Post(entry, uri, converter=douban.EventEntryFromString)

    def UpdateEvent(self, entry, content, title, invite_only=False, can_invite=True):
        if isinstance(entry, (str, unicode)):
            entry = self.Get(entry, douban.EventEntryFromString)
            
        entry.title = atom.Title(text=title)
        entry.content = atom.Content(text=content)
        entry.attribute.append(douban.Attribute('invite_only', invite_only and 'yes' or 'no'))
        entry.attribute.append(douban.Attribute('can_invite', can_invite and 'yes' or 'no'))
        uri = entry.GetSelfLink().href
        return self.Put(entry, uri, converter=douban.EventEntryFromString)

    def DeleteEvent(self, entry, reason):
        uri = entry.GetSelfLink().href+'/delete'
        entry = gdata.GDataEntry()
        entry.content = atom.Content(text=reason)
        return self.Post(entry, uri)

    def GetRecommendation(self, uri):
        return self.Get(uri, converter=douban.RecommendationEntryFromString)
 
    def GetRecommendations(self, uri, start_index=None, max_results=None):
        query = Query(uri, text_query=None, 
                    start_index=start_index, max_results=max_results)
        return self.Get(query.ToUri(), converter=douban.RecommendationFeedFromString)

    def AddRecommendation(self, title, url, comment=""):
        entry = douban.RecommendationEntry()
        entry.title = atom.Title(text=title)
        entry.link = atom.Link(href=url, rel="related")
        attribute = douban.Attribute('comment', comment)
        entry.attribute.append(attribute)
        return self.Post(entry, '/recommendations', converter=douban.RecommendationEntryFromString)

    def DeleteRecommendation(self, entry):
        return self.Delete(entry.id.text)

    def GetRecommendationComments(self, uri):
        return self.Get(uri, converter=douban.RecommendationCommentFeedFromString)

    def AddRecommendationComment(self, entry, comment):
        uri = entry.id.text+'/comments'
        entry = gdata.GDataEntry()
        entry.content = atom.Content(text=comment)
        return self.Post(entry, uri)

    def DeleteRecommendationComment(self, entry):
        return self.Delete(entry.id.text)

    def GetDoumail(self, uri):
        return self.Get(uri, converter=douban.DoumailEntryFromString)

    def GetDoumailFeed(self, uri):
        return self.Get(uri, converter=douban.DoumailFeedFromString)

    def AddDoumail(self, receiverURI, subject, body):
        entry = douban.DoumailEntry()
        entry.entity.append(douban.Entity('receiver', "",extension_elements=[atom.Uri(text=receiverURI)]))
        entry.title = atom.Title(text=subject)
        entry.content = atom.Content(text=body)

        return self.Post(entry, '/doumails', converter=douban.DoumailEntryFromString)

    def AddCaptchaDoumail(self, receiverURI, subject, body, captcha_token, captacha_string):
        entry = douban.DoumailEntry()
        entry.entity.append(douban.Entity('receiver', "",extension_elements=[atom.Uri(text=receiverURI)]))
        entry.title = atom.Title(text=subject)
        entry.content = atom.Content(text=body)
        entry.attribute = []
        entry.attribute.append(douban.Attribute('captcha_string', captacha_string))
        entry.attribute.append(douban.Attribute('captcha_token', captcha_token))
        return self.Post(entry, '/doumails', converter=douban.DoumailEntryFromString) 

    def DeleteDoumail(self, entry):
        uri = entry.GetSelfLink().href  
        return self.Delete(uri)

    def DeleteDoumails(self, uris):
        feed = gdata.GDataFeed()
        for uri in uris:
            entry = gdata.GDataEntry()
            entry.id = atom.Id(text=uri)
            feed.entry.append(entry)
        return self.Post(feed, '/doumail/delete')

    def MarkDoumailRead(self, uris):
        feed = gdata.GDataFeed()
        for uri in uris:
            entry = gdata.GDataEntry()
            entry.id = atom.Id(text=uri)
            entry.attribute = []
            entry.attribute.append(douban.Attribute('unread', 'false'))
            feed.entry.append(entry)
        return self.Put(feed, '/doumail/')

class Query(gdata.service.Query):
    def __init__(self, feed=None, text_query=None, start_index=None,
            max_results=None, **params):
        gdata.service.Query.__init__(self, feed=feed, text_query=text_query,
                params=params)
        if start_index is not None:
            self.start_index = start_index
        if max_results is not None:
            self.max_results = max_results
