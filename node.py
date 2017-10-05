from datetime import datetime


class Node(object):
    def __init__(self, url, url_id):
        self.url = url
        self.url_id = url_id
        self.neighbours = set()
        self.current_pr = [1.0]
        self.crawled_pr = [1.0]
        self.page_size = ""
        self.page_status_code = ""
        self.crawled_time = ""