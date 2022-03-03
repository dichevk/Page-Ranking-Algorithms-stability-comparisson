import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import copy
from HITS import *
from InDegree import *
from PageRank import *
from OrdinalPageRanks import *



# Generates n graphs of size k and saves them in text files
# Creates png of every graph
def graph_generator(n, k):
    for i in range(n):
        G = nx.scale_free_graph(k, alpha=0.41, beta=0.54, gamma=0.05, delta_in=0.2, delta_out=0, create_using=None,
                                seed=None)
        file = "graphs\\graph-O-{}".format(i)
        nx.write_adjlist(G, file)
        plt.clf()
        nx.draw(G, node_color='green', with_labels=True, node_size=500)
        plt.savefig("graphs\\graph-0-{}.png".format(i))


# Loads graphs from text files
# lower_bound is the numerical id of the first graph to be loaded
# upper_bound is the numerical id of the last graph to be loaded
# type is used to distinguish between original graphs, denoted by - O, and modified ones, denoted by - Mk, where k is an int.
def graph_loader(lower_bound, upper_bound, type):
    graphs = []
    for i in range(lower_bound, upper_bound + 1):
        file = "graphs\\graph-{}-{}".format(type.upper(), str(i))
        G = nx.read_adjlist(file, create_using=nx.DiGraph)
        graphs.append(G)

    return graphs


# Saves the graphs in the provided list of graphs - modified_graphs.
# k is int that denotes the size of change
def graph_saver(modified_graphs, k):
    i = 0
    for G in modified_graphs:
        file = "graphs\\graph-M{}-{}".format(k, str(i))
        nx.write_adjlist(G, file)
        plt.clf()
        nx.draw(G, node_color='green', with_labels=True, node_size=500)
        plt.savefig("graphs\\graph-M{}-{}.png".format(k, str(i)))
        i += 1


# @param n -> size of the graph
# @param k -> size of the change
def modify_graph(G, n, k):
    G1 = copy.deepcopy(G)
    removed_edges_dict = {}
    for node in G1.nodes:
        removed_edges_dict[node] = []

    rolled_nodes = []

    iteration_range = int(k / 2)
    i = 0
    while i < iteration_range:
        node1 = list(G1.nodes)[random.randint(0, n - 1)]
        if node1 not in rolled_nodes and len(list(G1.neighbors(node1))) > 0:
            rolled_nodes.append(node1)
            neighbours_node1 = [n for n in G1.neighbors(node1)]
            node2 = neighbours_node1[random.randint(0, len(neighbours_node1) - 1)]

            removed_edges_dict[node1].append(node2)

            G1.remove_edge(node1, node2)

            i += 1

    f = 0
    while f < iteration_range:
        new_node1 = list(G1.nodes)[random.randint(0, n - 1)]
        neighbours_new_node1 = [n for n in G1.neighbors(new_node1)]
        if len(set.union(set(neighbours_new_node1), set(removed_edges_dict[new_node1]))) == len(list(G1.nodes)):
            continue
        set_difference_list = list(
            set(list(G1.nodes)) - (set.union(set(neighbours_new_node1), set(removed_edges_dict[new_node1]))))
        new_node2 = set_difference_list[random.randint(0, len(set_difference_list) - 1)]
        G1.add_edge(new_node1, new_node2)
        f += 1

    return G1


def test_graph(k):
    graphs1 = graph_loader(0, 9, 'O')
    graphs2 = graph_loader(0, 9, 'M{}'.format(k))
    for i in range(0, 10):
        if len(set.union(set(graphs1[i].edges), set(graphs2[i].edges))) != len(list(graphs1[i].edges)) + int(k / 2):
            print('error at {}'.format(i))
            print("Length union: {}".format(len(set.union(set(graphs1[i].edges), set(graphs2[i].edges)))))
            print("Expected length: {}".format(len(list(graphs1[i].edges)) + int(k/2)))
            print("G1 - G2: ".format(set(graphs1[i].edges).difference(set(graphs2[i].edges))))
            print("G2 - G1: ".format(set(graphs2[i].edges).difference(set(graphs1[i].edges))))
            print("\n")


def graph_modifier(graphs, k):
    modified_graphs = []
    for G in graphs:
        modified_graphs.append(modify_graph(G, len(list(G.nodes)), k))

    return modified_graphs


def get_ordinal_ranks(num_iterations, types):
    os.remove("PageRank_results.txt")
    os.remove("HITS_results.txt")
    os.remove("In_Degree_results.txt")
    origin_graphs = graph_loader(0, 9, 'O')
    #dict key type value dict algorithm type : simscore arr

    for type in types:
        HITS_sim_scores_arr = []
        In_Degree_sim_scores_arr = []
        PageRank_sim_scores_arr = []
        largest_absolute_distance_PageRank = 0
        final_largest_change_PageRank = 0
        largest_absolute_distance_Indegree = 0
        final_largest_change_Indegree = 0
        largest_absolute_distance_HITS = 0
        final_largest_change_ = 0

        updated_graphs = graph_loader(0, 9, type)
        print("TYPE {}\n".format(type))
        for origin_graph, updated_graph in zip(origin_graphs, updated_graphs):
            '''
            print("PageRank for Graph {}".format(origin_graphs.index(origin_graph)))
            print(ordinal_ranks(page_rank(origin_graph, 0.85, num_iterations)))
            print("\n")
            print(ordinal_ranks(page_rank(updated_graph, 0.85, num_iterations)))
            print("\n\n")
            print("HITS for Graph {}".format(origin_graphs.index(origin_graph)))
            print(ordinal_ranks(hits(origin_graph, num_iterations)))
            print("\n")
            print(ordinal_ranks(hits(updated_graph, num_iterations)))
            print("\n\n")
            print("In Degree for Graph {}".format(origin_graphs.index(origin_graph)))
            print(ordinal_ranks(in_degree(origin_graph)))
            print("\n")
            print(ordinal_ranks(in_degree(updated_graph)))
            print("\n\n")
            '''


            abs_dist, largest_change = similarity_score(ordinal_ranks(page_rank(origin_graph, 0.85, num_iterations)),
                                 ordinal_ranks(page_rank(updated_graph, 0.85, num_iterations)))
            PageRank_sim_scores_arr.append((abs_dist, largest_change))
            abs_dist, largest_change = similarity_score(ordinal_ranks(in_degree(origin_graph)),
                                                         ordinal_ranks(in_degree(updated_graph)))
            In_Degree_sim_scores_arr.append((abs_dist,largest_change))
            abs_dist, largest_change = similarity_score(ordinal_ranks(hits(origin_graph, num_iterations)),
                                                    ordinal_ranks(hits(updated_graph, num_iterations)))
            HITS_sim_scores_arr.append((abs_dist, largest_change))

        with open("PageRank_results.txt", 'a') as file:
            file.write("Type: {}\n".format(type))
            for t in PageRank_sim_scores_arr:
                file.write("graph-{}-{} : absolute distance = {} | largest_change = {}\n".format(type, PageRank_sim_scores_arr.index(t), t[0], t[1]))
            file.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

        with open("In_Degree_results.txt", 'a') as file:
            file.write("Type: {}\n".format(type))
            for t in In_Degree_sim_scores_arr:
                file.write("graph-{}-{} : absolute distance = {} | largest_change = {}\n".format(type, In_Degree_sim_scores_arr.index(t), t[0], t[1]))
            file.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

        with open("HITS_results.txt", 'a') as file:
            file.write("Type: {}\n".format(type))
            for t in HITS_sim_scores_arr:
                file.write("graph-{}-{} : absolute distance = {} | largest_change = {}\n".format(type, HITS_sim_scores_arr.index(t), t[0], t[1]))
            file.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")





if __name__ == '__main__':
    '''
    graph_generator(10,10)
    graphs = graph_loader(0,9,"O")
    graph_saver(graph_modifier(graphs, 4), 4)
    graph_saver(graph_modifier(graphs, 6), 6)
    graph_saver(graph_modifier(graphs, 8), 8)
    print("Testing 4")
    test_graph(4)
    print("\n\nTesting 6")
    test_graph(6)
    print(" \n\nTesting 8")
    test_graph(8)
    '''
    get_ordinal_ranks(100, ['M4', 'M6', 'M8'])




