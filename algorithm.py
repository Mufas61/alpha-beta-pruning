import graphviz as gv
import logging

# was max/min
# cuts
# a/b


def alphabeta(graph, node, depth, isMaximizingPlayer, alpha, beta):
    """algo"""

    if type(graph[node]) is not list:
        return graph[node]  # value of the node

    if isMaximizingPlayer:
        bestVal = float("-inf")
        for child in graph[node]:
            value = alphabeta(graph, child, depth + 1, False, alpha, beta)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = float("inf")
        for child in graph[node]:
            value = alphabeta(graph, child, depth + 1, True, alpha, beta)
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal


def main():
    graph = {
        'A': ['B', 'C'],
        'B': 1,
        'C': 2,
    }

    f = alphabeta(graph, next(iter(graph)), 0, True, float("-inf"), float("inf"))
    print(f)

if __name__ == '__main__':
    main()