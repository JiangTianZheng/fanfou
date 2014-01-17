#!/usr/bin/env python
#-*- coding=utf-8 -*-

import sys, urllib, urllib2, re ,httplib
import oauth.oauth as oauth
import time
import uuid
import hmac
import time
import hashlib
import binascii
import urlparse
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

consumer_key       = "9eab891a46e90644738442f4c03d461b"
consumer_secret    = "acce8a65db9d239e8ba5d9865ac6a1d6"
oauth_token_key    = "1436156-3139ae61a2a46f72254ea00f1fbcfda1"
oauth_token_secret = "706fcb982ed0e5e21de71cf62c176006"
token="oauth_token_secret=706fcb982ed0e5e21de71cf62c176006&oauth_token=1436156-3139ae61a2a46f72254ea00f1fbcfda1"

signature_method   = oauth.OAuthSignatureMethod_HMAC_SHA1()
consumer           = oauth.OAuthConsumer(consumer_key, consumer_secret)
oauth_token        = oauth.OAuthToken(oauth_token_key, oauth_token_secret)

def request_to_header(request, realm=''):
    """Serialize as a header for an HTTPAuth request."""
    #auth_header = 'OAuth realm="%s"' % realm
    auth_header = 'OAuth realm="%s"' % realm
        # Add the oauth parameters.
    if request.parameters:
        for k, v in request.parameters.iteritems():
            if k.startswith('oauth_') or k.startswith('x_auth_'):
                auth_header += ', %s="%s"' % (k, oauth.escape(str(v)))
    return {'Authorization': auth_header}
    
def  get(url):
    url  = 'http://api.fanfou.com/%s.xml' %url
    request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                     token=oauth_token,
                                                     http_method='GET',
                                                     http_url=url,
                                                     parameters={})
    request.sign_request(signature_method, consumer, oauth_token)
    headers=request_to_header(request)
    req  = urllib2.Request(url, headers=headers)
    try:
        result    = urllib2.urlopen(req)
        code, xml = result.getcode(), result.read()
        if code==200:
            return xml
    except Exception,e:
        return 0
    
def  post(url,**args):
    url  = 'http://api.fanfou.com/%s.xml' %url
    data = args
    request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                     token=oauth_token,
                                                     http_method='POST',
                                                     http_url=url,
                                                     parameters=data)
    request.sign_request(signature_method, consumer, oauth_token)
    headers=request_to_header(request)
    data = urllib.urlencode(data)
    req  = urllib2.Request(url, data, headers=headers)
    try:
        result = urllib2.urlopen(req)
        code   = result.getcode()
        if code==200:
            return 1
    except Exception,e:
        return 0

def  post_photo():
    register_openers()
    url  = 'http://api.fanfou.com/photos/upload.xml' 
    f    = file('/var/www/fanfou/picture/1.jpg','rb')
    pic  = f.read()
    f.close()
    values = {'photo':pic}
    data, headers = multipart_encode(values)
    request = oauth.OAuthRequest.from_consumer_and_token(consumer,
                                                     token=oauth_token,
                                                     http_method='POST',
                                                     http_url=url,
                                                     parameters={})
    request.sign_request(signature_method, consumer, oauth_token)
    headers.update(request_to_header(request))
    #headers['Content-Type']='multipart/form-data'
    req  = urllib2.Request(url, data, headers=headers)
    req.unverifiable = True
    try:
        result = urllib2.urlopen(req)
        code   = result.getcode()
        if code==200:
            return 1
    except Exception,e:
        print e,e.code,e.read()
if __name__ == '__main__':
    post_photo()
