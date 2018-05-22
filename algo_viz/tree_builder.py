"""
Builder that provides methods to build tree-graphs. The graph are represented as a dictionary.
Example: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
"""
import math
import random


def build_random_leafs(depth=3, branching=3):
    """
    Builds a dict representation of a random generated graph.

    :param depth: Depth of the graph - int
    :param branching: Amount of branches  on each node - int
    :return: (order, graph) - (List[Key1, Key2, ...], Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...})
    """
    my_randoms = []
    for i in range(int(math.pow(branching, depth))):
        my_randoms.append(random.randrange(-99, 99, 1))

    return my_randoms


def build_graph(values, branching=2):
    """
    Builds a dict representation of a graph from a list of values for the leafs.

    :param values: Heuristics of the leaf nodes - list[int, int, ...]
    :param branching: Amount of branches on each node - int
    :return: (order, graph) - (List[Key1, Key2, ...], Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...})
    """
    length = len(list(values))
    if length not in [math.pow(branching, n) for n in range(100)]:  # TODO infinite range or something
        raise RuntimeError("Illegal Argument: values has to be an amount of the power of " + str(branching))

    graph = {}
    log = math.log(length, branching)
    global COUNTER
    COUNTER = 0
    __build_graph(graph, 'X', log, values, branching)

    order = sorted(graph, key=lambda k: (len(k), k.lower()))
    return order, graph


def __build_graph(result, node, length, values, branching_factor):
    # break condition
    if length == 0:
        global COUNTER
        result[node] = values[COUNTER]
        COUNTER += 1
        return

    childes = []
    for x in range(branching_factor):
        key = node + str(x)  # TODO max is a branching of 9. Node 10 will clash with Node 1-0
        childes.append(key)
        __build_graph(result, key, length - 1, values, branching_factor)
    result[node] = childes
