from algo_viz.utility import get_order


def min_max_sort(graph, root=None):
    """
    Mini-max algorithm.

    :param graph: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
    :param root: Node to start with
    :return: [<bestValue>, <DescriptionOfDoneOperations>]
    """
    my_root = root if root is not None else next(iter(graph))
    result_graph, _ = __min_max_sort(graph, {}, my_root, True)

    return result_graph, get_order(result_graph, my_root)


def __min_max_sort(graph, result_graph, node, is_maximizing_player):
    """
    :param graph: Dict{'<node>': [<node|leaf>, <node|leaf>], '<leaf>': <value>, ...}
    :param node: Node to start with
    :param is_maximizing_player: True/False
    :return: [<bestValue>, <DescriptionOfDoneOperations>]
    """
    # break condition - is a leaf?
    if type(graph[node]) is not list:
        result_graph[node] = graph[node]
        return result_graph, graph[node]  # value of the leaf

    children_best = {}

    if is_maximizing_player:
        best_val = float('-inf')

        for child in graph[node]:
            _, child_value = __min_max_sort(graph, result_graph, child, False)
            best_val = max(best_val, child_value)

            children_best[child] = best_val

        result_graph[node] = sorted(children_best, key=lambda k: children_best[k], reverse=True)

        return result_graph, best_val

    else:  # is minimizer
        best_val = float('inf')

        for child in graph[node]:
            _, child_value = __min_max_sort(graph, result_graph, child, True)
            best_val = min(best_val, child_value)

            children_best[child] = best_val

        result_graph[node] = sorted(children_best, key=lambda k: children_best[k])

        return result_graph, best_val
