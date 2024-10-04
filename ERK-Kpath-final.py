import random
import networkit as nk

from csv_writer import CsvWriter


def ERW_Kpath(G: nk.Graph, kappa: int, rho: int, beta: float):
    # Step 1: Assign each node its normalized degree
    normalized_degrees = {v: G.degree(v) / G.numberOfNodes() for v in G.iterNodes()}

    # Step 2: Assign each edge the uniform probability function as weight
    uniform_weight = 1.0 / G.numberOfEdges()
    for u, v in G.iterEdges():
        G.setWeight(u, v, uniform_weight)

    # Step 3-7: Main loop
    for _ in range(rho):
        vn = random.choice(list(G.iterNodes()))
        N = 0
        MessagePropagation(G, vn, N, kappa, beta)


def MessagePropagation(G: nk.Graph, vn: int, N: int, kappa: int, beta: float):
    T = {(min(u, v), max(u, v)): 0 for u, v in G.iterEdges()}  # Track visited edges using tuples for undirected edges

    while N < kappa and sum(1 for neighbor in G.iterNeighbors(vn) if T[(min(vn, neighbor), max(vn, neighbor))] == 0) > 0:
        # Select an unvisited edge
        unvisited_edges = [(vn, neighbor) for neighbor in G.iterNeighbors(vn) if T[(min(vn, neighbor), max(vn, neighbor))] == 0]
        em = random.choice(unvisited_edges)

        # Get the next node
        vn_next = em[1] if em[0] == vn else em[0]

        # Update edge weight
        current_weight = G.weight(em[0], em[1])
        G.setWeight(em[0], em[1], current_weight + beta)

        # Mark edge as visited
        T[(min(em[0], em[1]), max(em[0], em[1]))] = 1

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
    beta = 1.0 / G.numberOfEdges()  # Weight increment

    ERW_Kpath(G, kappa, rho, beta)

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