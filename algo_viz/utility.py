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


def get_order(graph, root):
    order = [root]
    return __get_order(graph, root, order)


def __get_order(graph, node, order):
    children = graph[node]

    if type(children) is list:
        order += children

        for child in children:
            __get_order(graph, child, order)

    return order
