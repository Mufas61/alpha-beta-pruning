import graphviz as gv
import logging


# was max/min
# cuts
# a/b


def alphabeta(graph, node, isMaximizingPlayer, alpha, beta, out):
    """alpha-beta-pruning that returns a describtion of done """

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
        return bestVal

    else:
        bestVal = float("inf")
        for child in graph[node]:
            value = alphabeta(graph, child, True, alpha, beta, out)
            bestVal = min(bestVal, value)  # best from child-nodes
            beta = min(beta, bestVal)
            out[child] = {"value": bestVal, "alpha": alpha, "beta": beta}
            if beta <= alpha:
                break  # (graph, child)  # actually break but we need to ????
        return bestVal


def test():
    graph = {
        'A': ['B', 'C'],
        'B': 1,
        'C': 2,
    }

    f = alphabeta(graph, next(iter(graph)), 0, True, float("-inf"), float("inf"))
    print(f)


if __name__ == '__main__':
    test()
