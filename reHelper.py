import re

class ReHelper(object):

    #Deprecated
    def get_google_url(self):
        return re.compile(r'\/url\?q\=(.+?)\&sa\=')

    #Deprecated
    def get_google_webcache_url(self):
        return re.compile(r'(https|http)\:\/\/(.+?)\.')

    #Get site name of a given url
    def get_site_name(self, url):
        pattern = re.compile(r'(https|http)\:\/\/(.+?)\/')
        try:
            re_obj = re.findall(pattern, url)[0]
            return re_obj[0]+'://'+re_obj[1]+'/'
        except:
            return url

    #Check if a url is valid
    def url_validator(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        try:
            return re.findall(regex, url)[0]
        except:
            return None