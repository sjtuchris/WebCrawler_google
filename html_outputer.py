import os
import errno


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self, keyword, url_id, data):
        dir = os.path.dirname(__file__)
        filename = os.path.join(dir, 'pages', keyword, str(url_id)+'.html')

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # filename = os.path.join(dir, 'pages', keyword, str(url_id)+'.html')
        fout = open(filename, 'w')
        fout.write(data)
        fout.close()

    def output_final_pr(self, keyword, page_rank, url_set, url_dict):
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
        fout.write("<body>")
        fout.write("<table>")
        fout.write("<tr>")
        fout.write("<td>%s</td>" % "Crawled_PR:&nbsp&nbsp")
        fout.write("<td>%s</td>" % "Final_PR:&nbsp&nbsp")
        fout.write("<td>%s</td>" % "Url:&nbsp&nbsp")
        fout.write("</tr>")

        for url in url_set:
            node = url_dict[url]
            fout.write("<tr>")
            fout.write("<td>%s</td>" % str(node.crawled_pr))
            fout.write("<td>%s</td>" % str(page_rank[node.url]))
            fout.write(("<td>%s</td>" % node.url).encode('utf-8'))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("<html>")

        fout.close()
