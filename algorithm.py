import math

import graphviz as gv

COLOR_FOR_CUTS = 'red'

COLOR_FOR_DEAD_NODES = 'grey'

NORMAL_COLOR = 'black'


def alpha_beta(graph):
    """
    Alpha-Beta-Pruning that returns a description of done operations.

    :param graph: Dict{'<node>': [<node|leaf>,<node|leaf>], '<leaf>': <value>, ...}
    :return: Dict{'<node>': {'value': <bestVal>, 'alpha': <alpha>, 'beta': <beta>}, ...}
    """
    start_node = next(iter(graph))
    best_val, out = _alpha_beta(graph, start_node, True, float("-inf"), float("inf"), {})

    # add leaf values
    for _, node in enumerate(graph):
        if type(graph[node]) is not list:
            out[node] = __dict_from(best_val=graph[node], alpha=0, beta=0)

    return out


def _alpha_beta(graph, node, is_maximizing_player, alpha, beta, out):
    """
    :param graph: Dict{'<node>': [<node|leaf>,<node|leaf>], '<leaf>': <value>, ...}
    :param node: '<node>'
    :param is_maximizing_player: True/False
    :param alpha:
    :param beta:
    :param out: Empty dictionary that will be used in recursion.
    :return: [<bestValue>, <DescriptionOfDoneOperations>]
    """
    # break condition - if is a leaf?
    if type(graph[node]) is not list:
        return graph[node], out  # value of the leaf

    if is_maximizing_player:
        best_val = float("-inf")
        for child in graph[node]:
            value, _ = _alpha_beta(graph, child, False, alpha, beta, out)
            best_val = max(best_val, value)  # best from child-nodes
            alpha = max(alpha, best_val)
            out[node] = __dict_from(best_val, alpha, beta)
            if beta <= alpha:
                break  # todo???
        return best_val, out

    else:
        best_val = float("inf")
        for child in graph[node]:
            value, _ = _alpha_beta(graph, child, True, alpha, beta, out)
            best_val = min(best_val, value)  # best from child-nodes
            beta = min(beta, best_val)
            out[node] = __dict_from(best_val, alpha, beta)
            if beta <= alpha:
                break
        return best_val, out


def build(graph, algo_desc):
    """
    Builds a visualization from a graph and a description from a algorithm.
    :param graph: Dict{'<node>': [<node|leaf>,<node|leaf>], '<leaf>': <value>, ...}, Ordering is important for the layer
    :param algo_desc: Dict{'<node>': {'value': <bestVal>, 'alpha': <alpha>, 'beta': <beta>}, ...}
    :return: A Digraph from GraphViz as PNG.
    """
    viz_graph = gv.Digraph(format='png')
    _build(viz_graph, graph, algo_desc)
    return viz_graph


def _build(viz_graph, edges, algo_desc):
    """
    :param viz_graph: From GraphViz
    :param edges: Dict{'<node>': [<node|leaf>,<node|leaf>], '<leaf>': <value>, ...}, Ordering is important for the layer
    :param algo_desc: Dict{'<node>': {'value': <bestVal>, 'alpha': <alpha>, 'beta': <beta>}, ...}
    :return: formatted viz_graph-param.
    """
    # BUILD NODES
    is_maximizer = False
    next_at, next_at_power_of = 1, 0
    for i, node_key in enumerate(edges):

        # if next layer
        if next_at == i + 1:
            next_at_power_of += 1
            next_at = math.pow(2, next_at_power_of)
            is_maximizer = not is_maximizer

        # has NOT been processed?
        best_value, alpha, beta = '', '', ''
        if node_key not in algo_desc:
            viz_graph.attr('node', color=COLOR_FOR_DEAD_NODES)
        else:
            viz_graph.attr('node', color=NORMAL_COLOR)
            best_value = algo_desc[node_key]["value"]
            alpha = algo_desc[node_key]["alpha"]
            beta = algo_desc[node_key]["beta"]

        # style and build current node
        if type(edges[node_key]) is list:  # multi edges
            viz_graph.attr('node', shape=('triangle' if is_maximizer else 'invtriangle'))
            viz_graph.node(node_key, str(best_value), xlabel='&alpha;= ' + str(alpha) + '; &beta;= ' + str(beta))
        else:
            viz_graph.attr('node', shape='square')
            viz_graph.node(node_key, str(best_value))

    # BUILD EDGES
    for i, node_key in enumerate(edges):
        # build edges
        if type(edges[node_key]) is list:  # multi edges
            for _, node_child in enumerate(edges[node_key]):

                # has been processed?
                if node_key not in algo_desc:
                    viz_graph.attr('edge', color=COLOR_FOR_DEAD_NODES, style='dotted')
                elif node_key in algo_desc and node_child not in algo_desc:
                    viz_graph.attr('edge', color=COLOR_FOR_CUTS, style='line')
                else:
                    viz_graph.attr('edge', color=NORMAL_COLOR, style='line')

                viz_graph.edge(node_key, node_child)


def __dict_from(best_val, alpha, beta):
    """
    Builds a description as dict for one node.

    :param best_val:
    :param alpha:
    :param beta:
    :return: {"value": <best_val>, "alpha": <alpha>, "beta": <beta>}
    """
    return {"value": best_val, "alpha": alpha, "beta": beta}


def test():
    edges = {
        'A': ['B', 'C'],  # 1. Layer
        'B': ['D', 'E'],  # 2. Layer
        'C': ['F', 'G'],
        'D': 1,  # 3. Layer
        'E': 2,
        'F': 3,
        'G': 4,
    }

    algo_desc = alpha_beta(edges)
    viz_graph = build(edges, algo_desc)
    print(viz_graph)


if __name__ == '__main__':
    test()
