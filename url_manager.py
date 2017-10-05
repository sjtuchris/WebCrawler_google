from node import Node
import collections
import reHelper
import robotparser
import urlparse


class UrlManager(object):

    def __init__(self):
        #Urls that are not yet crawled
        self.new_urls_queue = collections.deque()

        #Urls that are crawled
        self.old_urls_set = collections.deque()

        #All created nodes
        self.node_set = set()

        #Find a node with a url
        self.node_url_dict = dict()

        #Find a node with a url_id
        self.node_id_dict = dict()

        #Find a url_set which contains all urls belongs to a site
        self.site_url_set_dict = dict()

        #Find a site with a url
        self.url_site_dict = dict()

        #Find if a site is crawlable
        self.site_robot_dict = dict()

        self.re_helper = reHelper.ReHelper()

    def add_new_url(self, parent_url, url):
        if url is None or self.re_helper.url_validator(url) is None:
            return

        #Avoid duplicate urls
        if self.is_new_url(url):
            self.new_urls_queue.append(url)

            #If url is new, we need to create a new url node
            node = Node(url, len(self.node_set))
            self.node_set.add(node)
            self.node_url_dict[url] = node
            self.node_id_dict[node.url_id] = node
        else:
            node = self.node_url_dict[url]

        #Actually neighbours is a set of children urls.
        if parent_url is not None:
            parent_node = self.node_url_dict[parent_url]
            parent_node.neighbours.add(node)

    def add_new_urls(self, parent_url, urls, site_limit_num):
        if urls is None or len(urls) == 0:
            return

        #We don't want to change the original urls deque
        tmp = collections.deque(urls)

        #If certain site exceeds the limit number we set, we discard incoming urls that belongs to this site
        tmp = self.site_limitation_filter(tmp, site_limit_num)

        while tmp:
            url = tmp.popleft()
            self.add_new_url(parent_url, url)

    def has_new_url(self):
        return len(self.new_urls_queue) != 0

    #Get the first url in the queue, add it to crawled set and mark down its current PR value
    def get_new_url(self):
        new_url = self.new_urls_queue.popleft()
        new_node = self.node_url_dict[new_url]
        new_node.crawled_pr = new_node.current_pr
        self.old_urls_set.append(new_url)
        return new_url

    #Check if this url is crawled
    def is_new_url(self, url):
        if url not in self.new_urls_queue and url not in self.old_urls_set:
            return True

    #Filter a url if the num of visits of its site has already exceeded the limit
    def site_limitation_filter(self, urls, limit_num):
        tmp = collections.deque(urls)

        for url in urls:
            site_name = self.re_helper.get_site_name(url)

            if site_name in self.site_url_set_dict:
                if len(self.site_url_set_dict[site_name]) >= limit_num:
                    tmp.remove(url)
                else:
                    self.site_url_set_dict[site_name].add(url)
                    self.url_site_dict[url] = site_name
            else:
                self.site_url_set_dict[site_name] = set()
                self.site_url_set_dict[site_name].add(url)
                self.url_site_dict[url] = (site_name)

        return tmp

    #Validate the robot protocol
    def robot_validator(self, url):
        site_name = self.url_site_dict[url]

        try:

            #To improve the performance, we put the robot parser in a dict,
            #so that we don't need to get robot.txt multiple times for the same site
            if site_name not in self.site_robot_dict:
                self.site_robot_dict[site_name] = self.robot_parser_generator(site_name)
            if not self.site_robot_dict[site_name].can_fetch("*", url):
                print "This site is robot exclusive!\n"
                return False
            return True
        except:
            return True

    #Generate a robot parser
    def robot_parser_generator(self, site):
        parser = robotparser.RobotFileParser()
        parser.set_url(urlparse.urljoin(site, 'robots.txt'))
        parser.read()
        return parser
