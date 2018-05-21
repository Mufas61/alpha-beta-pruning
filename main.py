"""
Runs a test for debugging.
"""
import graphviz as gv
from IPython.core.display import display, Image

from algo_viz.algorithm import alpha_beta
from algo_viz.tree_builder import build_graph
from algo_viz.utility import print_pretty
from algo_viz.visualizer import build_viz


def test():
    order, graph2 = build_graph([10, 8, 7, 12, 9, 6, 4, 17, 20], branching_factor=3)
    print_pretty(graph2, order)

    desc = alpha_beta(graph2, root=order[0])
    print_pretty(desc, order)

    viz = build_viz(order, graph2, desc, branching_factor=3)

    if type(viz) is gv.Graph:
        print("PASSED!")
    else:
        print("ERR")


def test2():
    graph = {
        # 1. Layer
        'X': ['A', 'B'],
        # 2. Layer
        'A': ['AA', 'AB'],
        'B': ['BA', 'BB'],
        # 3. Layer
        'AA': ['AAA', 'AAB'],
        'AB': ['ABA', 'ABB'],
        'BA': ['BAA', 'BAB'],
        'BB': ['BBA', 'BBB'],
        # 4. Layer
        'AAA': 10,
        'AAB': 8,
        'ABA': 7,
        'ABB': 12,
        'BAA': 9,
        'BAB': 6,
        'BBA': 4,
        'BBB': 17,
    }
    desc = alpha_beta(graph)
    print_pretty(desc)
    digraph = build_viz(graph.keys(), graph, desc, branching_factor=2)
    digraph.render(filename='img/graph')
    display(Image(filename='img/graph.png'))

if __name__ == '__main__':
    test2()
