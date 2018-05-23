def print_pretty(dict, order=None):
    """
    Prints a graph in a pretty form.
    :param order:
    :param dict:
    :return: a pretty printed graph
    """
    if order is None:
        print("{ ")
        for _, edge in enumerate(dict):
            print("   " + str(edge) + ": " + str(dict[edge]))
        print("}")
    else:
        print("{ ")
        for elem in order:
            try:
                print("   " + str(elem) + ": " + str(dict[elem]))
            except:
                print("   " + str(elem) + ": None")
        print("}")


def sort(leaf_values, depth=2, branching=2, maximizer=True):
    mid = len(leaf_values) / 2
    x1 = list[:mid]
    x2 = list[mid:]

    result = sort(max(min(x1), min(x2)))

    return result
