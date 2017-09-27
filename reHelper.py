import re

class ReHelper(object):

    def get_google_url(self):
        return re.compile(r'\/url\?q\=(.+?)\&sa\=')

    def get_google_webcache_url(self):
        return re.compile(r'(https|http)\:\/\/(.+?)\.')