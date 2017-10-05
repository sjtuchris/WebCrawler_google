from crawl_orchestrator import SpiderOrchestrator

if __name__ == "__main__":
    print "Roger that, Apocalypse Crawler starts:\n"

    keyword = raw_input("Input your keyword: ")
    keyword = keyword.replace(" ", "+")
    crawl_total_num = input("Input crawl num: ")
    site_limit_num = 10

    print "Keyword: %s" % keyword
    print "Num: %d" % crawl_total_num

    root_url = "https://www.googleapis.com/customsearch/v1?" \
                     "key=AIzaSyDB3ertl7fWzilApD5-R0qdt0cRbxpOBaU&cx=018378841471714571048:q0s65ecluiq&q=" \
                     + keyword + "&num=10"

    # root_url = "https://www.googleapis.com/customsearch/v1?" \
    #            "key=AIzaSyA-R0htMg0kowOWhn7NZj028ek7ECsimUU&cx=018378841471714571048:fsokcy1abd0&q=" \
    #            + keyword + "&num=10"

    objSpider = SpiderOrchestrator()
    objSpider.craw(keyword, root_url, crawl_total_num, site_limit_num)
