from datetime import datetime
import traceback
import collections
import urllib2
import url_manager, html_downloader, html_google_fetcher, html_outputer, html_parser, page_rank_util


class SpiderOrchestrator(object):
    def __init__(self):
        self.url_manager = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.google_fetcher = html_google_fetcher.HtmlGoogleParser()
        self.pr_calculator = page_rank_util.PRCalculator()
        self.url_parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    #Change parameters of a url node, mainly used for exception cases
    def node_update_attr(self, new_url, page_size, page_status_code, crawled_time):
        self.url_manager.node_url_dict[new_url].page_size = page_size
        self.url_manager.node_url_dict[new_url].page_status_code = page_status_code
        self.url_manager.node_url_dict[new_url].crawled_time = crawled_time

    #Perform page rank and update url queue so that url with higher page rank would be crawled first
    def page_rank_performer(self, node_set, node_id_dict, new_urls_queue, new_urls):

        page_rank = self.pr_calculator.page_rank(node_set,
                                                 node_id_dict,
                                                 new_urls)

        self.url_manager.new_urls_queue = self.pr_calculator. \
            update_new_urls_queue(page_rank, new_urls_queue)

        return page_rank

    #Main craw logic
    def craw(self, keyword, root_url, crawl_total_num, site_limit_num):
        crawl_count = 1
        file_count = 0
        size_count = 0
        start_time = datetime.now()
        pr_trigger_num = 0
        page_rank = []
        blakclist = ['.cgi', '.pdf', '.mp4', '.mp3', '.asp']
        self.url_manager.add_new_url(None, root_url)

        while self.url_manager.has_new_url():
            new_url = self.url_manager.get_new_url()
            try:
                print "craw %d : %s" % (crawl_count, new_url)

                #Robot exclusion
                if crawl_count > 11:
                    if not self.url_manager.robot_validator(new_url):
                        self.node_update_attr(new_url, "Null", "Anti_Robot", str(datetime.now()))
                        continue

                #Blacklist
                try:
                    if new_url[-4:] in blakclist or '.cgi' in new_url:
                        self.node_update_attr(new_url, "Null", "Blacklist", str(datetime.now()))
                        continue
                except:
                    pass

                #For Google Api limit usage, the local json can be used just for testing
                # if crawl_count == 1:
                #     html_cont = open('nyu.json', 'r').read()
                #     page_size = 1
                #     page_type = 'text/html'
                #     page_status_code = 200
                # else:
                #     html_cont, page_size, page_type, page_status_code = self.downloader.download(new_url)

                html_cont, page_size, page_type, page_status_code = self.downloader.download(new_url)

                #Only crawl text/html pages, skip others such as cgi, pdf, jpg etc.
                if not page_type == 'text/html' and crawl_count > 1:
                    self.node_update_attr(new_url, "Null", "Not_Html", str(datetime.now()))
                    print "Not html page, skip!"
                    continue

                self.node_update_attr(new_url, page_size, page_status_code, str(datetime.now()))

                #The start page parser is different from other pages
                if crawl_count == 1:
                    new_urls, new_data = self.google_fetcher.get_google_urls(new_url, html_cont)
                else:
                    new_urls, new_data = self.url_parser.parse(new_url, html_cont)

                #Filter duplicate urls
                new_urls = collections.deque(set(new_urls))

                #Many actions required when adding new urls, details can be found in url_manager class
                self.url_manager.add_new_urls(new_url, new_urls, site_limit_num)

                #Page Rank
                pr_trigger_num += 1
                if pr_trigger_num >= 0.05 * len(page_rank):
                    page_rank = self.page_rank_performer(self.url_manager.node_set,
                                             self.url_manager.node_id_dict,
                                             self.url_manager.new_urls_queue,
                                             new_urls)

                    pr_trigger_num = 0

                #Save crawled pages
                url_id = self.url_manager.node_url_dict[new_url].url_id
                self.outputer.output_html(keyword, url_id, new_data)

                print "Page saved!\n"
                file_count += 1
                size_count += page_size

                #Ouput final report
                if crawl_count == crawl_total_num:
                    time_count = (datetime.now() - start_time).total_seconds()
                    page_rank = self.page_rank_performer(self.url_manager.node_set,
                                                         self.url_manager.node_id_dict,
                                                         self.url_manager.new_urls_queue,
                                                         new_urls)

                    self.outputer.output_final_pr(keyword, page_rank,
                                                  file_count, size_count, time_count,
                                                  self.url_manager.old_urls_set,
                                                  self.url_manager.node_url_dict)

                    break
                crawl_count += 1

            except urllib2.HTTPError, err:
                #Catch HTTP error
                node = self.url_manager.node_url_dict[new_url]
                node.page_status_code = str(err.code)
                node.crawled_time = str(datetime.now())

            except:
                print traceback.print_exc()
                print "craw fail\n"