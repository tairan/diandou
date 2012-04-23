# -*- encoding:utf-8 -*-

import httplib,urlparse,cgi
import time
import oauth

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

API_HOST = 'http://api.douban.com'
AUTH_HOST = 'http://www.douban.com'
REQUEST_TOKEN_URL = AUTH_HOST+'/service/auth/request_token'
ACCESS_TOKEN_URL = AUTH_HOST+'/service/auth/access_token'
AUTHORIZATION_URL = AUTH_HOST+'/service/auth/authorize'

class OAuthClient:
    def __init__(self, server='www.douban.com', key=None, secret=None):
        self.server = server
        self.consumer = oauth.OAuthConsumer(key, secret)
        self.token = None

    def login(self, key=None, secret=None):
        if key and secret:
            self.token = oauth.OAuthToken(key, secret)
            return True

        key,secret = self.get_request_token()
        if not key:
            print 'get request token failed'
            return 
        url = self.get_authorization_url(key, secret)
        print 'please paste the url in your webbrowser, complete the authorization then come back:'
        print url
        line = raw_input()
        
        key, secret, uid = self.get_access_token(key, secret)
        if key:
            return self.login(key, secret)
        else:
            print 'get access token failed'
            return False

    def fetch_token(self, oauth_request):
        connection = httplib.HTTPConnection("%s:%d" % (self.server, 80))
        connection.request('GET', urlparse.urlparse(oauth_request.http_url).path,
            headers=oauth_request.to_header())
        response = connection.getresponse()
        r = response.read()
        try:
            token = oauth.OAuthToken.from_string(r)
            params = cgi.parse_qs(r, keep_blank_values=False)
            user_id = params.get('douban_user_id',[None])[0]
            return token.key,token.secret, user_id
        except:
            return None,None,None

    def get_request_token(self):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                        http_url=REQUEST_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, None)
        return self.fetch_token(oauth_request)[:2]

    def get_authorization_url(self, key, secret, callback=None):
        token = oauth.OAuthToken(key, secret)
        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, 
                http_url=AUTHORIZATION_URL, callback=callback)
        return oauth_request.to_url()
 
    def get_access_token(self, key=None, secret=None, token=None):
        if key and secret:
            token = oauth.OAuthToken(key, secret)
        assert token is not None
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=token, http_url=ACCESS_TOKEN_URL)
        oauth_request.sign_request(signature_method, self.consumer, token)
        return self.fetch_token(oauth_request)[:3]
 
    def get_auth_header(self, method, uri, parameter={}):
        if self.token:
            if not uri.startswith('http'):
                uri = API_HOST + uri
            oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                    token=self.token, http_method=method, http_url=uri, parameters=parameter)
            oauth_request.sign_request(signature_method, self.consumer, self.token)
            return oauth_request.to_header()
        else:
            return {}
 
    def access_resource(self, method, url, body=None):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, 
                token=self.token, http_url=url)
        oauth_request.sign_request(signature_method, self.consumer, self.token)
        headers = oauth_request.to_header()
        if method in ('POST','PUT'):
            headers['Content-Type'] = 'application/atom+xml; charset=utf-8'
        connection = httplib.HTTPConnection("%s:%d" % (self.server, 80))
        connection.request(method, url, body=body,
            headers=headers)
        return connection.getresponse()


def test():
    API_KEY = '' 
    SECRET = ''
    client = OAuthClient(key=API_KEY, secret=SECRET)
    client.login()
    res = client.access_resource('GET', 'http://api.douban.com/test?a=b&c=d').read()
    print res

if __name__ == '__main__':
    test()
