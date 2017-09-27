from page_rank_util import Node
import collections


class UrlManager(object):

    def __init__(self):
        self.new_urls_set = set()
        self.new_urls_queue = collections.deque()
        self.old_urls_set = collections.deque()
        self.node_set = set()
        self.node_url_dict = dict()
        self.node_id_dict = dict()

    def add_new_url(self, parent_url, url):
        if url is None:
            return

        if self.is_new_url(url):
            self.new_urls_queue.append(url)
            self.new_urls_set.add(url)

            node = Node(url, len(self.node_set))
            self.node_set.add(node)
            self.node_url_dict[url] = node
            self.node_id_dict[node.url_id] = node
        else:
            node = self.node_url_dict[url]

        if parent_url is not None:
            parent_node = self.node_url_dict[parent_url]
            parent_node.neighbours.add(node)

    def add_new_urls(self, parent_url, urls):
        if urls is None or len(urls) == 0:
            return
        tmp = collections.deque(urls)
        while tmp:
            url = tmp.popleft()
            self.add_new_url(parent_url, url)

    def has_new_url(self):
        return len(self.new_urls_queue) != 0

    def get_new_url(self):
        new_url = self.new_urls_queue.popleft()
        new_node = self.node_url_dict[new_url]
        new_node.crawled_pr = new_node.current_pr
        self.new_urls_set.remove(new_url)
        self.old_urls_set.append(new_url)
        return new_url

    def is_new_url(self, url):
        if url not in self.new_urls_set and url not in self.old_urls_set:
            return True
