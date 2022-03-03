# Takes: graph 'G' and number of iterations 'i'
# Returns: a dictionary of the form {page_name: page_rank}
def hits(G, i):
    authority_scores = dict()
    hub_scores = dict()

    # Initialization of hub scores for all nodes.
    for p in G.nodes:
        hub_scores[p] = 1

    while i != 0:

        # Calculation of authority scores of all nodes.
        for p in G.nodes:
            authority_scores[p] = 0
            for h in G.in_edges(p):
                authority_scores[p] += hub_scores[h[0]]

        # Calculation of hub scores of all nodes based on the previously calculated authority scores
        for p in G.nodes:
            hub_scores[p] = 0
            for a in G.out_edges(p):
                hub_scores[p] += authority_scores[a[1]]

        i -= 1

    total_authority_score = 0
    total_hub_score = 0

    for p in G.nodes:
        total_authority_score += authority_scores[p]    # Getting the total of all authority scores
        total_hub_score += hub_scores[p]    # Getting the total of all hub scores

    for p in G.nodes:
        authority_scores[p] /= total_authority_score    # Downscaling all authority scores
        hub_scores[p] /= total_hub_score    # # Downscaling all hub scores

    return authority_scores
