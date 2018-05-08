import graphviz as gv

# was max/min
# cuts
# a/b


def test():


def build(graph, layout):
    """layout -> graph"""
    g2 = gv.Digraph(format='png')
    # maximizer nodes
    g2.attr('node', shape='triangle')
    g2.node('max-1', label='A')
    # minimizer nodes
    g2.attr('edge', shape='invtriangle')
    g2.node('min-2', label='B')
    g2.node('min-3', label='C')
    # add edges
    g2.edge('max-1', 'min-2', label='&alpha;=-&infin;; &beta;=&infin;')
    g2.attr('edge', color='red', style='dotted')
    g2.edge('max-1', 'min-3', label='&alpha;=-&infin;; &beta;=&infin;')
    return {}
