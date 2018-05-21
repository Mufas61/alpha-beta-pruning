"""
Alpha-beta-pruning algorithm.
"""


def alpha_beta(graph, root=None):
    """
    Alpha-Beta-Pruning that returns a description of done operations.

    :param graph: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
    :param root: Node to start with.
    :return: Dict{'<node>': {'value': <bestVal>, 'alpha': <alpha>, 'beta': <beta>}, ...}
    """
    _, out = __alpha_beta(graph,
                          root if root is not None else next(iter(graph.values())),
                          True,
                          float("-inf"),
                          float("inf"), {})

    return out


def __alpha_beta(graph, node, is_maximizing_player, alpha, beta, out):
    """
    :param graph: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
    :param node: '<node>'
    :param is_maximizing_player: True/False
    :param alpha:
    :param beta:
    :param out: Empty dictionary that will be used in recursion.
    :return: [<bestValue>, <DescriptionOfDoneOperations>]
    """
    # break condition - if is a leaf?
    if type(graph[node]) is not list:
        out[node] = __dict_from(graph[node], 0, 0)
        return graph[node], out  # value of the leaf

    if is_maximizing_player:
        best_val = float("-inf")
        for child in graph[node]:
            value, _ = __alpha_beta(graph, child, False, alpha, beta, out)
            best_val = max(best_val, value)  # best from child-nodes
            alpha = max(alpha, best_val)
            out[node] = __dict_from(best_val, alpha, beta)
            if beta <= alpha:
                break
        return best_val, out

    else:
        best_val = float("inf")
        for child in graph[node]:
            value, _ = __alpha_beta(graph, child, True, alpha, beta, out)
            best_val = min(best_val, value)  # best from child-nodes
            beta = min(beta, best_val)
            out[node] = __dict_from(best_val, alpha, beta)
            if beta <= alpha:
                break
        return best_val, out


def __dict_from(best_val, alpha, beta):
    """
    Helper-method that builds a description as dict for one node.

    :return: {"value": <best_val>, "alpha": <alpha>, "beta": <beta>}
    """
    return {"value": best_val, "alpha": alpha, "beta": beta}
