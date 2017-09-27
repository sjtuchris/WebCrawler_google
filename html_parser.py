from bs4 import BeautifulSoup
import collections
import urlparse

class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = collections.deque()
        links = soup.find_all('a')
        count = 0

        for link in links:
            new_url = link.get('href')
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.append(new_full_url)
            count += 1

            #No more than 30 links per site
            if count >= 30:
                break

        return new_urls

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        return new_urls, html_cont