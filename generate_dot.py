import json

import networkx as nx


def main():
    with open("implications.json") as f:
        implications = json.load(f)

    # Remove non-approved implications
    implications = [impl for impl in implications if impl["status"] == 2]

    # Group implications by connected clusters with NetworkX
    digraph = nx.DiGraph()
    for impl in implications:
        digraph.add_edge(
            impl["predicateTag"]["name"],
            impl["consequentTag"]["name"]
        )
    graph = digraph.to_undirected()
    subgraphs = map(digraph.subgraph, nx.connected_components(graph))
    # list of subgraphs, each subgraph is a list of edge-tuples
    subgraphs_edges = [sg.edges() for sg in subgraphs]

    # Output in Dot format for rendering with Graphviz
    print("digraph {")
    print("    splines = true")
    print("    rankdir = LR")
    print()
    for i, edges in enumerate(subgraphs_edges):
        print(f"    subgraph cluster{i} {{")
        for src, dst in edges:
            print(f'''        "{src}" -> "{dst}"''')
        print("    }")
    print("}")


if __name__ == "__main__":
    main()
