import urllib2


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        response = urllib2.urlopen(url, None, headers)

        if response.getcode() != 200:
            return None

        return response.read()