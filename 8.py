import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_with_path(G, shortest_path, title, path_edges):
    plt.figure(figsize=(8, 5))
    pos = nx.spring_layout(G)
    
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', alpha=0.7)
    
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)
    
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='orange', width=2)
    
    nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color='orange', node_size=700)

    nx.draw_networkx_labels(G, pos, font_size=15)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): w for u, v, w in G.edges(data='weight')})
    
    plt.title(title)
    plt.axis('off')
    plt.show()

G_undirected = nx.Graph()
G_undirected.add_edges_from([(1, 2), (2, 3), (3, 1), (3, 4)])

shortest_path_undirected = nx.dijkstra_path(G_undirected, source=1, target=4)
shortest_path_edges_undirected = [(shortest_path_undirected[i], shortest_path_undirected[i + 1]) for i in range(len(shortest_path_undirected) - 1)]
draw_graph_with_path(G_undirected, shortest_path_undirected, "Basic Undirected Graph with Shortest Path Highlighted", shortest_path_edges_undirected)

G_directed = nx.DiGraph()
G_directed.add_edges_from([(1, 2), (2, 3), (3, 4), (1, 4)])

shortest_path_directed = nx.dijkstra_path(G_directed, source=1, target=4)
shortest_path_edges_directed = [(shortest_path_directed[i], shortest_path_directed[i + 1]) for i in range(len(shortest_path_directed) - 1)]
draw_graph_with_path(G_directed, shortest_path_directed, "Directed Graph with Shortest Path Highlighted", shortest_path_edges_directed)

G_weighted = nx.Graph()
edges_weighted = [(1, 2, 1), (1, 3, 4), (2, 3, 2), (2, 4, 5), (3, 4, 1)]
G_weighted.add_weighted_edges_from(edges_weighted)

shortest_path_weighted = nx.dijkstra_path(G_weighted, source=1, target=4)
shortest_path_edges_weighted = [(shortest_path_weighted[i], shortest_path_weighted[i + 1]) for i in range(len(shortest_path_weighted) - 1)]
draw_graph_with_path(G_weighted, shortest_path_weighted, "Weighted Graph with Dijkstra's Shortest Path Highlighted", shortest_path_edges_weighted)

G_bellman = nx.Graph()
edges_bellman = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 2), (2, 3, 3)]
G_bellman.add_weighted_edges_from(edges_bellman)

try:
    source_bellman, target_bellman = 0, 3
    shortest_path_bellman = nx.bellman_ford_path(G_bellman, source_bellman, target_bellman)
    shortest_path_edges_bellman = [(shortest_path_bellman[i], shortest_path_bellman[i + 1]) for i in range(len(shortest_path_bellman) - 1)]
    draw_graph_with_path(G_bellman, shortest_path_bellman, "Weighted Graph with Bellman-Ford's Shortest Path Highlighted", shortest_path_edges_bellman)
except nx.NetworkXUnbounded:
    print("Negative cycle detected in Bellman-Ford graph!")

G_astar = nx.Graph()
edges_astar = [(1, 2, 2), (1, 3, 5), (2, 3, 1), (2, 4, 3), (3, 5, 2), (4, 5, 1)]
G_astar.add_weighted_edges_from(edges_astar)

def heuristic(a, b):
    return abs(a - b)

shortest_path_astar = nx.astar_path(G_astar, source=1, target=5, heuristic=heuristic)
shortest_path_edges_astar = [(shortest_path_astar[i], shortest_path_astar[i + 1]) for i in range(len(shortest_path_astar) - 1)]
draw_graph_with_path(G_astar, shortest_path_astar, "Weighted Graph with A* Shortest Path Highlighted", shortest_path_edges_astar)

G_complex = nx.Graph()
complex_edges = [
    (1, 2, 3), (1, 3, 1), (1, 4, 4), 
    (2, 3, 1), (2, 5, 6), 
    (3, 4, 2), (3, 5, 1),
    (4, 5, 2)
]
G_complex.add_weighted_edges_from(complex_edges)

dijkstra_path = nx.dijkstra_path(G_complex, source=1, target=5)
dijkstra_path_edges = [(dijkstra_path[i], dijkstra_path[i + 1]) for i in range(len(dijkstra_path) - 1)]

astar_path = nx.astar_path(G_complex, source=1, target=5, heuristic=heuristic)
astar_path_edges = [(astar_path[i], astar_path[i + 1]) for i in range(len(astar_path) - 1)]

bellman_path = nx.bellman_ford_path(G_complex, source=1, target=5)
bellman_path_edges = [(bellman_path[i], bellman_path[i + 1]) for i in range(len(bellman_path) - 1)]

plt.figure(figsize=(12, 8))
pos_complex = nx.spring_layout(G_complex)
nx.draw_networkx_edges(G_complex, pos_complex, edge_color='lightgray', alpha=0.7)
nx.draw_networkx_nodes(G_complex, pos_complex, node_color='lightblue', node_size=700)

nx.draw_networkx_edges(G_complex, pos_complex, edgelist=dijkstra_path_edges, edge_color='orange', width=2)
nx.draw_networkx_nodes(G_complex, pos_complex, nodelist=dijkstra_path, node_color='orange', node_size=700)

nx.draw_networkx_edges(G_complex, pos_complex, edgelist=astar_path_edges, edge_color='green', width=2)
nx.draw_networkx_nodes(G_complex, pos_complex, nodelist=astar_path, node_color='green', node_size=700)

nx.draw_networkx_edges(G_complex, pos_complex, edgelist=bellman_path_edges, edge_color='red', width=2)
nx.draw_networkx_nodes(G_complex, pos_complex, nodelist=bellman_path, node_color='red', node_size=700)

nx.draw_networkx_labels(G_complex, pos_complex, font_size=15)
nx.draw_networkx_edge_labels(G_complex, pos_complex, edge_labels={(u, v): w for u, v, w in complex_edges})

plt.title("Comparing Shortest Paths: Dijkstra (Orange), A* (Green), Bellman-Ford (Red)")
plt.axis('off')
plt.show()
