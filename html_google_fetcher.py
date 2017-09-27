import json
import collections

class HtmlGoogleParser(object):

    def get_google_urls(self, page_url, json_cont):
        if page_url is None or json_cont is None:
            return

        links = json.loads(json_cont)["items"]
        new_urls = collections.deque()

        for link in links:
            new_urls.append(link["link"])

        return new_urls, json_cont