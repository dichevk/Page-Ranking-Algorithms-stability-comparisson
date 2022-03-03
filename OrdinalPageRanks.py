# Takes: page_rank dictionary
# Returns: tuples of the form (position, page_name, ordinal_page_rank)
def ordinal_ranks(ranks):
    tuples = []
    position = 1
    for p in ranks:
        tuples.append((p, ranks[p], position))  # (page_name, page_rank, position)
        position += 1
    # We sort the list of tuples by 2 criteria,
    # namely page_rank and position (their relative position in the network data structure)
    tuples = sorted(tuples, key=lambda x: x[1], reverse=True)   # Sorting by page_rank in descending order.
    tuples = ordinal_sort(tuples)   # Sorting by position in ascending order.

    ordinal_page_ranks = []
    # Constructing new list of tuples in the form (position, page_name, ordinal_page_rank)
    # that will represent our ordinal ranking vector.
    for t in tuples:
        ordinal_page_ranks.append((t[2], t[0], tuples.index(t)+1))  # (position, page_name, ordinal_page_rank)
    ordinal_page_ranks = sorted(ordinal_page_ranks, key=lambda x: x[0], reverse=False)

    return ordinal_page_ranks


# Takes list 'unsorted_list' of sorted by page_rank in descending order tuples
# of the form - (page_name, page_rank, position)
# Returns: 'unsorted_list' sorted by position.
def ordinal_sort(unsorted_list):
    index = int()   # Starting index of the sublist with page_rank 'x'
    result = []
    x = -1     # Tuple page_rank

# The code below goes through the sorted tuples in the list, finds the starting and ending position
# of every sublist of tuple(s) that have the same page_rank, sorts them by position and
# appends every sublist to a new list 'result' that stores the sorted sub-lists.
    for t in unsorted_list:
        if x == -1:     # With the first element of the list we initialize all necessary variables.
            x = t[1]
            index = unsorted_list.index(t)
            continue
        elif x != t[1]:     # If we find new sublist with different page_rank
            result += sorted(unsorted_list[index:unsorted_list.index(t)],
                             key=lambda y: y[2], reverse=False)    # We sort the previous sublist
            x = t[1]    # Save the page_rank of the new sublist
            index = unsorted_list.index(t)  # Save starting index of the new sublist

    result += sorted(unsorted_list[index:],
                     key=lambda y: y[2], reverse=False)  # We make sure that last sublist is also sorted and added
    return result


# Takes: 2 ordinal_page_rank lists of tuples
# Returns: the absolute distance between the ordinal_page_ranking tuples
def similarity_score(ordinal_page_ranks1, ordinal_page_ranks2):
    absolute_distance = 0
    largest_change = 0

    for p, k in zip(ordinal_page_ranks1, ordinal_page_ranks2):
        absolute_distance += abs(p[2] - k[2])
        if largest_change < abs(p[2] - k[2]):
            largest_change = abs(p[2] - k[2])

    return absolute_distance, largest_change

