import collections
import numpy as np


class PRCalculator(object):
    __doc__ = '''Calculate_Page_Rank'''

    def __init__(self):
        self.damping_factor = 0.85
        self.max_iterations = 100
        self.min_delta = 0.000001

    def page_rank(self, node_set, node_id_dict, new_urls):
        graph_size, page_rank, page_neighbours_graph = self.initialize(node_set, node_id_dict, new_urls)

        if graph_size == 0:
            return {}

        #Using random jump to avoid sink
        damping_value = (1.0 - self.damping_factor) / graph_size
        flag = False
        count = 0

        for i in range(self.max_iterations):
            tmp = page_rank

            page_rank = damping_value + self.damping_factor * \
                                        (page_neighbours_graph.dot(page_rank))

            change = np.sum(np.abs(tmp - page_rank))

            if change < self.min_delta:
                print graph_size
                flag = True
                count = i + 1
                break

        if flag:
            print "Page Rank finished in %s iterations!" % count
        else:
            print "Page Rank finished out of 100 iterations!"
        return self.page_rank_array_to_dict(page_rank, node_id_dict)

    #Initialize page rank graph
    def initialize(self, node_set, node_id_dict, new_urls):
        N = len(node_set)
        page_rank = (np.ones((N), dtype=np.float)*1.0/N).reshape(-1, 1)
        page_neighbours_graph = np.zeros((N, N), dtype=np.float)
        for col in range(N):
            node = node_id_dict[col]
            neighbours = node.neighbours
            neighbours_num = len(node.neighbours)

            #Deal with leak situation
            if neighbours_num == 0:
                page_neighbours_graph[:, col] = 1.0/N
            else:
                for neighbour in neighbours:
                    page_neighbours_graph[neighbour.url_id, col] = 1.0/neighbours_num

        return N, page_rank, page_neighbours_graph

    #Util to transform array to dict
    def page_rank_array_to_dict(self, page_rank_array, node_id_dict):
        if len(page_rank_array) == 0:
            return {}

        page_rank = dict()
        for i in range(len(page_rank_array)):
            node = node_id_dict[i]
            node.current_pr = page_rank_array[i]
            page_rank[node.url] = page_rank_array[i]

        return page_rank

    def update_new_urls_queue(self, page_rank, new_urls_queue):
        '''
        Update new_urls_queue based on the new page_rank
        :param page_rank:
        :param new_urls_queue:
        :return: updated queue
        '''
        new_urls_dict = dict()
        updated_new_urls_queue = collections.deque()

        for url in page_rank:
            if url in new_urls_queue:
                new_urls_dict[url] = page_rank[url]

        #Sort the elements in the queue only, instead of sort all nodes in the graph
        for i in sorted(new_urls_dict, key=new_urls_dict.get, reverse=True):
            updated_new_urls_queue.append(i)

        # print "Page Rank Value:"
        # print new_urls_dict
        return updated_new_urls_queue
