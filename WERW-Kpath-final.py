import random
import networkit as nk
from networkit import Graph

from csv_writer import CsvWriter


def assign_normalized_degree(G: Graph):
    degrees = {}
    total_nodes = G.numberOfNodes()
    for node in G.iterNodes():
        degree = G.degree(node)
        normalized_degree = degree / total_nodes
        degrees[node] = normalized_degree
    return degrees


def initialize_weights(G: Graph):
    for u, v in G.iterEdges():
        G.setWeight(u, v, 1)


def WERW_KPath(G: Graph, kappa: int, rho: int):
    normalized_degrees = assign_normalized_degree(G)
    initialize_weights(G)

    for _ in range(rho):
        vn = random.choices(list(G.iterNodes()), weights=list(normalized_degrees.values()), k=1)[0]
        N = 0
        MessagePropagation(G, vn, N, kappa)

    # Normalize edge weights
    for u, v in G.iterEdges():
        G.setWeight(u, v, G.weight(u, v) / rho)


def MessagePropagation(G: Graph, vn: int, N: int, kappa: int):
    T = {(u, v): 0 for u, v in G.iterEdges()}  # Track visited edges

    while N < kappa and sum(1 for e in G.iterNeighbors(vn) if T.get((vn, e), 0) == 0) > 0:
        # Select an unvisited edge based on weights
        unvisited_edges = [(vn, e) for e in G.iterNeighbors(vn) if T.get((vn, e), 0) == 0]

        if not unvisited_edges:
            break

        edge_weights = [G.weight(e[0], e[1]) for e in unvisited_edges]
        em = random.choices(unvisited_edges, weights=edge_weights, k=1)[0]

        # Get the next node
        vn_next = em[1]

        # Update edge weight
        G.setWeight(em[0], em[1], G.weight(em[0], em[1]) + 1)

        # Mark edge as visited
        T[em] = 1
        T[(em[1], em[0])] = 1  # Mark both directions for undirected graph

        # Move to next node
        vn = vn_next
        N += 1

def main():
    # Load graph
    reader = nk.graphio.EdgeListReader(separator=" ", firstNode=0, continuous=False, directed=False)
    G = reader.read("./graph/2expedge(n=640, m=639).txt")

    # Algorithm parameters
    kappa = 3  # Maximum path length
    rho = G.numberOfEdges()  # Number of iterations

    WERW_KPath(G, kappa, rho)  # Remove the beta parameter


    edge_centrality = [(u, v, G.weight(u, v)) for u, v in G.iterEdges()]

    edge_centrality_sorted = sorted(edge_centrality, key=lambda x: x[2], reverse=True)


    print("Edge Centrality Values (sorted):")
    csv_data = []
    for u, v, weight in edge_centrality_sorted:
        dict_csv_row = {"edge": f"{u}, {v}", "centrality": weight}
        csv_data.append(dict_csv_row)
        print(f"Edge ({u}, {v}): {weight}")
    CsvWriter().write(csv_data, "./csv_files/time", ["edge", "centrality"])

if __name__ == "__main__":
    main()
