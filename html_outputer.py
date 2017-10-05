import os
import errno


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    #Ouput html pages
    def output_html(self, keyword, url_id, data):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'pages', keyword, str(url_id)+'.html')

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        fout = open(filename, 'w')
        fout.write(data)
        fout.close()

    #Generate final report
    def output_final_pr(self, keyword, page_rank, file_count, size_count,
                        time_count, url_set, url_dict):

        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'pages', keyword + '.html')

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        fout = open(filename, 'w')

        fout.write("<html>")
        fout.write("<head>")
        fout.write("<style>")
        fout.write("table, th, td")
        fout.write("{border: 1px solid black; border - collapse: collapse;}")
        fout.write("</style>")
        fout.write("</head>")
        fout.write("<body>")
        fout.write("<table style='width:100%'>")

        fout.write("<tr>")
        fout.write("<td>%s</td>" % "File count:")
        fout.write("<td>%s</td>" % "Size count(MB):")
        fout.write("<td>%s</td>" % "Time count(min):")
        fout.write("</tr>")

        fout.write("<tr>")
        fout.write("<td>%s</td>" % file_count)
        fout.write("<td>%s</td>" % str(size_count/1024/1024))
        fout.write("<td>%s</td>" % str(time_count/60))
        fout.write("</tr>")

        fout.write("<tr>")
        fout.write("<td>%s</td>" % "Page_code:")
        fout.write("<td>%s</td>" % "Page_Size:")
        fout.write("<td>%s</td>" % "Crawled_PR:")
        fout.write("<td>%s</td>" % "Final_PR:")
        fout.write("<td>%s</td>" % "Crawled_time:")
        fout.write("<td>%s</td>" % "Url:")
        fout.write("</tr>")

        for url in url_set:
            node = url_dict[url]
            # if not node.page_size:
            #     continue
            fout.write("<tr>")
            fout.write("<td>%s</td>" % str(node.page_status_code))
            fout.write("<td>%s</td>" % str(node.page_size))
            fout.write("<td>%s</td>" % str(node.crawled_pr[0]))
            fout.write("<td>%s</td>" % str(page_rank[node.url][0]))
            fout.write("<td>%s</td>" % str(node.crawled_time))
            fout.write(("<td>%s</td>" % node.url).encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("<html>")

        fout.close()
