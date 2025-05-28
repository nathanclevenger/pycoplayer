# Visualization script for module dependencies
# This script requires networkx and matplotlib.
# Run `pip install networkx matplotlib` if not already installed.

import os
import ast

try:
    import networkx as nx
    import matplotlib.pyplot as plt
except ImportError as e:
    raise SystemExit('Missing dependencies: {}'.format(e))

def parse_imports(path):
    with open(path, 'r') as f:
        tree = ast.parse(f.read(), filename=path)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    return imports

def build_graph(src_dir='src'):
    G = nx.DiGraph()
    modules = {}
    for filename in os.listdir(src_dir):
        if filename.endswith('.py'):
            module = os.path.splitext(filename)[0]
            modules[module] = os.path.join(src_dir, filename)
    for module, path in modules.items():
        G.add_node(module)
        for imp in parse_imports(path):
            if imp in modules:
                G.add_edge(module, imp)
    return G

def main():
    G = build_graph()
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000,
            node_color='skyblue', edge_color='gray', arrowsize=20)
    plt.title('Module Dependency Graph')
    plt.show()

if __name__ == '__main__':
    main()
