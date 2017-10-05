from datetime import datetime
import url_manager, html_downloader, html_google_fetcher, html_outputer, html_parser, page_rank_util
import traceback
import collections


class Spider_BFS(object):
    def __init__(self):
        self.url_manager = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.google_fetcher = html_google_fetcher.HtmlGoogleParser()
        self.pr_calculator = page_rank_util.PRCalculator()
        self.url_parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def page_rank_performer(self, node_set, node_id_dict, new_urls_queue, new_urls):

        page_rank = self.pr_calculator.page_rank(node_set,
                                                 node_id_dict,
                                                 new_urls)

        self.url_manager.new_urls_queue = self.pr_calculator. \
            update_new_urls_queue(page_rank, new_urls_queue)

        return page_rank

    def craw(self, keyword, root_url, crawl_total_num, site_limit_num):
        count = 1
        pr_trigger_num = 0
        page_rank = []
        self.url_manager.add_new_url(None, root_url)

        while self.url_manager.has_new_url():
            new_url = self.url_manager.get_new_url()
            try:
                print "craw %d : %s" % (count, new_url)

                if count > 1:
                    if not self.url_manager.robot_validator(new_url):
                        continue
                #For Google Api limit usage
                if count == 1:
                    html_cont = open('nyu.json', 'r').read()
                    page_size = 1
                    page_type = 'text/html'
                else:
                    html_cont, page_size, page_type = self.downloader.download(new_url)

                if not page_type == 'text/html':
                    print "Not html page, skip!"
                    continue

                self.url_manager.node_url_dict[new_url].page_size = page_size

                if count == 1:
                    new_urls, new_data = self.google_fetcher.get_google_urls(new_url, html_cont)
                else:
                    new_urls, new_data = self.url_parser.parse(new_url, html_cont)

                #Filter duplicate urls
                new_urls = collections.deque(set(new_urls))

                self.url_manager.add_new_urls(new_url, new_urls, site_limit_num)
                #
                # pr_trigger_num += 1
                # if pr_trigger_num >= 0.05 * len(page_rank):
                #     page_rank = self.page_rank_performer(self.url_manager.node_set,
                #                              self.url_manager.node_id_dict,
                #                              self.url_manager.new_urls_queue,
                #                              new_urls)
                #
                #     pr_trigger_num = 0
                #     # print self.url_manager.new_urls_queue

                url_id = self.url_manager.node_url_dict[new_url].url_id
                self.outputer.output_html(keyword, url_id, new_data)

                print "Page saved!\n"

                if count == crawl_total_num:
                    page_rank = self.page_rank_performer(self.url_manager.node_set,
                                                         self.url_manager.node_id_dict,
                                                         self.url_manager.new_urls_queue,
                                                         new_urls)
                    self.outputer.output_final_pr(keyword, page_rank,
                                                  self.url_manager.old_urls_set,
                                                  self.url_manager.node_url_dict)
                    break
                count += 1
            # except urllib2.HTTPError, err:
            #     if err.code == 404 or err.code == 403:
            #         self.url_manager.remove_url(new_url)
            except:
                print traceback.print_exc()
                print "craw fail\n"