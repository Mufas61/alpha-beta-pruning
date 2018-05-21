import math

import graphviz as gv

SELECT_EDGE = 'edge'

SELECT_NODE = 'node'

COLOR_FOR_CUTS = 'red'

COLOR_FOR_DEAD_NODES = 'grey'

NORMAL_EDGE_COLOR = 'deepskyblue3'
NORMAL_NODE_COLOR = 'deepskyblue2'

COUNTER = 0


def build_viz(order, graph, algo_desc, branching_factor=2):
    """
    Builds a visualization from a graph and a description from a algorithm.

    :param order:
    :param graph: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}, Ordering is important for the layer
    :param algo_desc: Dict{'<node>': {'value': <bestVal>, 'alpha': <alpha>, 'beta': <beta>}, ...}
    :param branching_factor: Amount of branches on each node.
    :return: A graph from GraphViz as PNG.
    """
    viz_graph = gv.Graph(format='png')
    __build_viz(viz_graph, order, graph, algo_desc, branching_factor)
    return viz_graph


def __build_viz(viz_graph, order, edges, algo_desc, branching_factor):  # todo :param base
    """
    :param viz_graph: A graph from GraphViz as PNG
    :param order: Sorted list of the nodes. Is important for the layer
    :param edges: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
    :param algo_desc: Dict{'<node>': {'value': <bestVal>, 'alpha': <alpha>, 'beta': <beta>}, ...}
    :return: formatted viz_graph-param.
    """
    # BUILD NODES
    is_maximizer = True
    counter = 1
    next_at, next_at_power_of = 1, 0
    for node_key in order:
        # has NOT been processed?
        best_value, xlabel = '', ''
        viz_graph.attr(SELECT_NODE, style='filled', fontname='calibri', fontsize='12')
        if node_key not in algo_desc:
            viz_graph.attr(SELECT_NODE, color=COLOR_FOR_DEAD_NODES)
        else:
            viz_graph.attr(SELECT_NODE, color=NORMAL_NODE_COLOR)
            best_value = algo_desc[node_key]["value"]
            alpha = algo_desc[node_key]["alpha"]
            beta = algo_desc[node_key]["beta"]
            xlabel = '&alpha;:' + str(alpha) + ', &beta;:' + str(beta)

        # style and build current node
        if type(edges[node_key]) is list:  # multi edges
            viz_graph.attr(SELECT_NODE, shape=('triangle' if is_maximizer else 'invtriangle'))
            viz_graph.node(node_key, label=str(best_value) + '\n' + xlabel)
        else:
            viz_graph.attr(SELECT_NODE, shape='square')
            viz_graph.node(node_key, str(best_value))

        #  if next layer
        if next_at == counter:  # todo outsource
            next_at_power_of += 1
            next_at = math.pow(branching_factor, next_at_power_of)
            is_maximizer = not is_maximizer
            counter = 1
        else:
            counter += 1

    # BUILD EDGES
    for _, node_key in enumerate(edges):
        # build edges
        if type(edges[node_key]) is list:  # multi edges
            for _, node_child in enumerate(edges[node_key]):

                # has been processed?
                viz_graph.attr(SELECT_EDGE, arrowhead='none')
                if node_key not in algo_desc:
                    viz_graph.attr(SELECT_EDGE, color=COLOR_FOR_DEAD_NODES, style='dashed')
                elif node_key in algo_desc and node_child not in algo_desc:
                    viz_graph.attr(SELECT_EDGE, color=COLOR_FOR_CUTS, style='dashed')
                else:
                    viz_graph.attr(SELECT_EDGE, color=NORMAL_EDGE_COLOR, style='line')

                viz_graph.edge(node_key, node_child)
