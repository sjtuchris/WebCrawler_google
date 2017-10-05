from bs4 import BeautifulSoup
import collections
import urlparse

class HtmlParser(object):

    #Get hyperlink in this page
    def _get_new_urls(self, page_url, soup):
        new_urls = collections.deque()
        links = soup.find_all('a')

        for link in links:
            new_url = link.get('href')
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.append(new_full_url)

        return new_urls

    #Get new urls and content of this page
    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        return new_urls, html_cont