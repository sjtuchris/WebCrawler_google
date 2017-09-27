import url_manager, html_downloader, html_google_fetcher, html_outputer, html_parser, page_rank_util
import traceback
import collections


class SpiderMain(object):
    def __init__(self):
        self.url_manager = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.google_fetcher = html_google_fetcher.HtmlGoogleParser()
        self.pr_calculator = page_rank_util.PRCalculator()
        self.url_parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url, num):
        count = 1
        self.url_manager.add_new_url(None, root_url)

        while self.url_manager.has_new_url():
            try:
                new_url = self.url_manager.get_new_url()

                print "craw %d : %s" % (count, new_url)

                #No more than 30 links per site, details can be found in html_parser.py
                html_cont = self.downloader.download(new_url)
                if count == 1:
                    new_urls, new_data = self.google_fetcher.get_google_urls(new_url, html_cont)
                else:
                    new_urls, new_data = self.url_parser.parse(new_url, html_cont)

                #Filter duplicate urls
                new_urls = collections.deque(set(new_urls))

                self.url_manager.add_new_urls(new_url, new_urls)
                print new_urls

                page_rank = self.pr_calculator.page_rank(self.url_manager.node_set,
                                                         self.url_manager.node_id_dict,
                                                         new_urls)
                self.url_manager.new_urls_queue = self.pr_calculator.\
                    update_new_urls_queue(page_rank, self.url_manager.new_urls_set)

                # print self.url_manager.new_urls_set
                # print "Ranked new urls list:"
                # print "%s\n" % self.url_manager.new_urls_queue

                url_id = self.url_manager.node_url_dict[new_url].url_id
                self.outputer.output_html(keyword, url_id, new_data)

                print "Page saved!"

                if count == num:
                    self.outputer.output_final_pr(keyword, page_rank,
                                                  self.url_manager.old_urls_set,
                                                  self.url_manager.node_url_dict)
                    break
                count += 1
            except:
                print traceback.print_exc()
                print "craw fail"

if __name__ == "__main__":
    print "Roger that, Apocalypse Crawler starts:\n"

    keyword = "cat"
    keyword = keyword.replace(" ", "+")
    num = 10

    print "Keyword: %s" % keyword
    print "Num: %d" % num

    root_url = "https://www.googleapis.com/customsearch/v1?" \
                     "key=AIzaSyDB3ertl7fWzilApD5-R0qdt0cRbxpOBaU&cx=018378841471714571048:q0s65ecluiq&q=" \
                     + keyword + "&num=10"

    objSpider = SpiderMain()
    objSpider.craw(root_url, num)
