
def min_max(graph, root=None):
    """
    Mini-max algorithm.

    :param graph: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
    :param root: Node to start with
    :return: [<bestValue>, <DescriptionOfDoneOperations>]
    """
    return __min_max(graph, root if root is not None else next(iter(graph)), True)


def __min_max(graph, node, is_maximizing_player):
    """
    :param graph: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
    :param node: Node to start with
    :param is_maximizing_player: True/False
    :return: [<bestValue>, <DescriptionOfDoneOperations>]
    """
    # break condition - is a leaf?
    if type(graph[node]) is not list:
        return graph[node]  # value of the leaf

    if is_maximizing_player:
        best_val = float('-inf')
        for child in graph[node]:
            child_value = __min_max(graph, child, False)
            best_val = max(best_val, child_value)

        return best_val

    else:  # is minimizer
        best_val = float('inf')
        for child in graph[node]:
            child_value = __min_max(graph, child, True)
            best_val = min(best_val, child_value)

        return best_val
