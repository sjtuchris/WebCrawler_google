from timeout import timeout
import urllib2


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers = {'User-Agent': user_agent, }
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request, timeout = 10)

        if response.getcode() != 200:
            return None

        result = response.read()
        page_size = len(result)
        page_type =  response.info().type
        page_status_code = 200

        return result, page_size, page_type, page_status_code