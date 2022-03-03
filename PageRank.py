# Takes: graph 'G', Beta coefficient 's' and number of iterations 'i'
# Returns: a dictionary of the form {page_name: page_rank}
def page_rank(G, s, i):
    page_ranks = dict()     # Used to store final page_ranks after every iteration
    temporary_ranks = dict()    # Used to store the newly calculated page_ranks of the current iteration
    initial_rank = 1/len(G.nodes)   # Giving each page initial rank equal to 1/n, where n = number of pages in the graph
    for p in G.nodes:   # Giving initial ranks to all pages = 1/N(umber of pages)
        page_ranks[p] = initial_rank
        temporary_ranks[p] = 0  # Making sure that every page has an entry in the dictionary 'temporary_ranks'

    while i != 0:
        for k in temporary_ranks:   # Resetting all page_ranks in 'temporary_ranks' in the beginning of every iteration
            temporary_ranks[k] = 0
        for p in G.nodes:
            if G.out_degree(p) != 0:    # If page points to other pages
                rank_division = page_ranks[p] / G.out_degree(p)     # Proportion of rank that every succeeding page gets
                for n in G.neighbors(p):    # Applying 's' page_rank proportions and distributing it to succeeding pages
                    temporary_ranks[n] += rank_division * s
            else:   # In case of no succeeding pages, i.e no outgoing links from that page.
                temporary_ranks[p] += page_ranks[p] * s     # Applying 's' to the page_rank of the page and giving it back to itself


        for p in temporary_ranks:   # Distributing the remaining page_rank of (1 - s) to all pages and saving the resulting ranks to 'page_ranks' dictionary
            temporary_ranks[p] += (1 - s) / len(G.nodes)
            page_ranks[p] = temporary_ranks[p]
        i -= 1

    return page_ranks
