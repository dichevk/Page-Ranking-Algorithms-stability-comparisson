# Takes: a graph 'G'
# Returns: a dictionary of the form {page_name: page_rank}
def in_degree(G):
    in_degree_ranks = dict()
    for p in G.nodes():
        in_degree_ranks[p] = G.in_degree(p)     # page_rank of a page = number of edges pointing to it

    return in_degree_ranks
