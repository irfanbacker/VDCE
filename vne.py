import networkx as nx
import random
import graph
from graph import Parameters


def create_vne(min_nodes=2, max_nodes=3, probability=0.4):
    random_node_no = random.randint(min_nodes, max_nodes)
    G = nx.erdos_renyi_graph(random_node_no, probability, directed=False)
    ng = nx.to_dict_of_lists(G)
    g = {}
    for i in ng:
        g[i + 1] = []
        for j in ng[i]:
            g[i + 1].append(j + 1)

    if not nx.is_connected(G):
        null_node_list = [key for key, val in g.items() if not val]
        graph_node_count = {_key: len(_val) for _key, _val in g.items()}
        sorted_dict_list = sorted(
            graph_node_count.items(), key=lambda x: x[1], reverse=True
        )
        if len(null_node_list) != len(g):
            for index, empty_node in enumerate(null_node_list):
                g[sorted_dict_list[index][0]].append(empty_node)
                g[empty_node].append(sorted_dict_list[index][0])
        else:
            for i in range(len(g)):
                for j in range(len(g) - i - 1):
                    if null_node_list[j + 1] not in g[null_node_list[j]]:
                        g[null_node_list[j]].append(null_node_list[j + 1])
                    if null_node_list[j] not in g[null_node_list[j + 1]]:
                        g[null_node_list[j + 1]].append(null_node_list[j])

    # print("new VNE REQ is",new_vne_req)
    edges = set()
    nodes = len(g)
    for j in range(nodes):
        for k in g[j + 1]:
            edges.add((str(j), str(k - 1)))
    return graph.Graph(nodes, edges, 100,Parameters(1, 10, 1, 10, 0, 100, 0, 100, 1, 4)) # for vne request BW ,CRB, Location,Delay


if __name__ == "__main__":
    create_vne()