import math

import graphviz as gv

COLOR_FOR_CUTS = 'grey'

NORMAL_COLOR = 'black'


def alpha_beta(graph):
    """
    Alpha-Beta-Pruning that returns a description of done operations.
    :param graph: Dict{'<node>': [<node|leaf>,<node|leaf>], '<leaf>': <value>, ...}
    :return: Dict{'<node>': {'value': <bestVal>, 'alpha': <alpha>, 'beta': <beta>}, ...}
    """
    _, out = _alpha_beta(graph, next(iter(graph)), True, float("-inf"), float("inf"), {})
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
    val = graph[node]
    if type(val) is not list:  # is leaf?
        return graph[node], out  # value of the node

    if is_maximizing_player:
        best_val = float("-inf")
        for child in graph[node]:
            value, _ = _alpha_beta(graph, child, False, alpha, beta, out)
            best_val = max(best_val, value)  # best from child-nodes
            alpha = max(alpha, best_val)
            out[child] = {"value": best_val, "alpha": alpha, "beta": beta}
            if beta <= alpha:
                break  # todo???
        return best_val, out

    else:
        best_val = float("inf")
        for child in graph[node]:
            value, _ = _alpha_beta(graph, child, True, alpha, beta, out)
            best_val = min(best_val, value)  # best from child-nodes
            beta = min(beta, best_val)
            out[child] = {"value": best_val, "alpha": alpha, "beta": beta}
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
    # build nodes
    is_maximizer = False
    next_at_power_of = 0
    next_at = 1
    for i, node_key in enumerate(edges):

        # if next layer
        if next_at == i + 1:  # TODO save for better runtime?
            next_at_power_of += 1
            next_at = math.pow(2, next_at_power_of)
            is_maximizer = not is_maximizer

        # style current node
        if type(edges[node_key]) is list:  # multi edges
            viz_graph.attr('node', shape=('triangle' if is_maximizer else 'invtriangle'))
        else:
            viz_graph.attr('node', shape='square')

        # has NOT been processed?
        best_value, alpha, beta = '', '', ''
        if node_key not in algo_desc:
            viz_graph.attr('node', color=COLOR_FOR_CUTS)
        else:
            viz_graph.attr('node', color=NORMAL_COLOR)
            best_value = algo_desc[node_key]["value"]
            alpha = algo_desc[node_key]["alpha"]  # todo
            beta = algo_desc[node_key]["beta"]

        # build current node
        viz_graph.node(node_key, label=str(node_key) + ": " + str(best_value))

    # build edges
    for i, node_key in enumerate(edges):
        # has NOT been processed?
        if node_key not in algo_desc:
            viz_graph.attr('edge', color=COLOR_FOR_CUTS, style='dotted')
        else:
            viz_graph.attr('edge', color=NORMAL_COLOR, style='line')

        # build edges
        if type(edges[node_key]) is list:  # multi edges
            for _, node_child in enumerate(edges[node_key]):
                viz_graph.edge(node_key, node_child)


def test():
    edges = {
        'A': ['B', 'C'],
        'B': 1,
        'C': 2,
    }

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
