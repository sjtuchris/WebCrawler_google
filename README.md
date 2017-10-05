# WebCrawler_google
A web crawler based on page rank algorithms.


In command line: 

	pip install robotparser
	pip install urllib2
	pip install numpy

	python spider_main.py

Then: 

	Input the keyword and number of pages you would like to fetch

Note that keyword can only contain characters and space

Descriptions:

	Main parts in this project are shown below:

	spider_main.py: input keyword and number of pages you would like to crawl.

	spider_orchestrator:

		craw function:
			1. robot.txt check, if violate the protocol, just continue to the next url in queue
			2. download the content and get all urls in this page
			3. remove duplicate urls and give new urls to url_manager to handle them
			4. run page rank among all urls
			5. save pages locally
			6. catch http errors and ignore other errors
			7. if end, run page rank for all of the pages and generate a final report

	url_manager:

		add_new_url:
			1. check if url is valid
			2. check if url was crawled before
				if not: 
					add it to waiting_to_be_crawled queue
					create new url object and update related dictionaries
			3. update url neighbours dictionary

		add_new_urls:
			1. for each url, check if we have already crawled enough pages from the site that the url belongs to. If yes, we remove this url and will not crawl it.
			2. add each new url using add_new_url function

		has_new_url:
			check if we still have urls to crawl

		get_new_url:
			pick the first element from the url queue to crawl, and mark it as crawled

		site_limitation_filter: described in add_new_urls

		robot_validator: check url's robot protocol

		robot_parser_generator: create robotparser object and save it in memory

	Page_rank_util:

		page_rank: using numpy vector to implement page rank algorithm, "sink" is avoided by implementing random jump using a damping value

		initialize: create page rank graph. To avoid "leak", we assume the leak node has links to every node in our graph.

		update_new_urls_queue: update the waiting_to_be_crawled url queue based on the result of the page rank.

Features:
	
	Url validation: invalid urls are filtered.

	Cgi problem: only text/html content will be downloaded.

	Earlier visits: maintain dictionaries to keep track, it will never crawl a url twice.

	Site limition: maintain a site visit history, if one site is crawled too many times (exceed the limit), urls in this site will not be crawled.

	Exception: Crawler will not get stuck, but might stay in some site for a little bit long time

	









