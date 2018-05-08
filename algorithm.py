import graphviz as gv
import logging


# was max/min
# cuts
# a/b


def alphabeta(graph, node, isMaximizingPlayer, alpha, beta, out):
    """alpha-beta-pruning that returns a description of done operations"""

    if type(graph[node]) is not list:
        return graph[node]  # value of the node

    if isMaximizingPlayer:
        bestVal = float("-inf")
        for child in graph[node]:
            value = alphabeta(graph, child, False, alpha, beta, out)
            bestVal = max(bestVal, value)  # best from child-nodes
            alpha = max(alpha, bestVal)
            out[child] = {"value": bestVal, "alpha": alpha, "beta": beta}
            if beta <= alpha:
                break  # cut(graph, child)  # actually break but we need to ????
        return out

    else:
        bestVal = float("inf")
        for child in graph[node]:
            value = alphabeta(graph, child, True, alpha, beta, out)
            bestVal = min(bestVal, value)  # best from child-nodes
            beta = min(beta, bestVal)
            out[child] = {"value": bestVal, "alpha": alpha, "beta": beta}
            if beta <= alpha:
                break  # (graph, child)  # actually break but we need to ????
        return out


def build(edges, desc):
    """(edges as dict, layout, isMaximizer) -> graph for visualization"""
    viz_graph = gv.Digraph(format='png')
    _build(viz_graph, edges, desc, 0, True)
    return viz_graph


def _build(viz_graph, edges, desc, depth, isMaximizer):
    for i, node in enumerate(edges):

        # style current node
        viz_graph.attr('node', shape=('triangle' if isMaximizer else 'invtriangle'))

        # has been processed?
        bestValue = ""
        if node in desc:
            bestValue = desc[node]["value"]
            alpha = desc[node]["alpha"]  # todo
            beta = desc[node]["beta"]

        curr_name = str(depth) + "" + str(i)
        viz_graph.node(curr_name, label=str(bestValue))

        # viz edges
        if type(edges[node]) is list:
            for j in edges[node]:
                next_name = str(depth) + "" + str(j)
                viz_graph.edge(curr_name, next_name)

        _build(viz_graph, edges[node], desc, depth + 1, not isMaximizer)


def test():
    edges = {
        'A': ['B', 'C'],
        'B': 1,
        'C': 2,
    }

    desc = alphabeta(edges, next(iter(edges)), True, float("-inf"), float("inf"), {})
    viz_graph = build(edges, desc)
    print(viz_graph)


if __name__ == '__main__':
    test()
