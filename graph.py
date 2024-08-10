from typing import Dict
from node import Node
import networkx as nx
import matplotlib.pyplot as plt

class Edge:
    def __init__(self, node1: Node, node2: Node, viable_score: float):
        self.node1 = node1
        self.node2 = node2
        self.viable_score = viable_score


class Graph:
    def __init__(self, vertexList: Dict[Node, Dict[Node, Edge]] = None):
            self.vertexList = vertexList

    def createEdge(self, node1: Node, node2: Node, viable_score: float):
        if node1 not in self.vertexList:
            self.vertexList[node1] = {}
        if node2 not in self.vertexList:
            self.vertexList[node2] = {}
        
        edge = Edge(node1, node2, viable_score)
        self.vertexList[node1][node2] = edge
        self.vertexList[node2][node1] = edge

    def updateEdge(self, node1: Node, node2: Node, new_score: float):
        if node1 in self.vertexList and node2 in self.vertexList[node1]:
            self.vertexList[node1][node2].viable_score = new_score
            self.vertexList[node2][node1].viable_score = new_score
        else:
            raise KeyError(f"Edge does not exist.")

    def incidentEdges(self, node: Node) -> Dict[Node, Edge]:
        if node in self.vertexList:
            return self.vertexList[node]
        
    def vertexList(self) -> Dict[Node, Dict[Node, Edge]]:
        return self.vertexList

    def visualize_graph(self):
        G = nx.Graph()

        for node, edges in self.vertexList.items():
            for neighbor, edge in edges.items():
              G.add_edge(str(node), str(neighbor), weight=edge.viable_score)
    
        pos = nx.spectral_layout(G)

        nx.draw_networkx_nodes(G, pos, node_size=650)
        nx.draw_networkx_edges(G, pos, width=6)
        nx.draw_networkx_labels(G, pos, font_size=7, font_family='sans-serif')

        # AI start
        edge_labels = {(str(edge.node1), str(edge.node2)): f"{edge.viable_score}" for node in self.vertexList for edge in self.incidentEdges(node).values()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        # AI end

        plt.axis('off')
        plt.show()

#testing
# nodeA = Node(1)
# nodeB = Node(2)
# nodeC = Node(3)

# vertexList = {}

# nodeA = Node(1)
# nodeB = Node(2)
# nodeC = Node(3)
# graph = Graph(vertexList)
# graph.createEdge(nodeA, nodeB, 1.0)
# graph.createEdge(nodeA, nodeC, 2.0)
# graph.createEdge(nodeB, nodeC, 21.0)

# graph.visualize_graph()

# print(graph.incidentEdges(nodeA))
# print(graph.incidentEdges(nodeB))
# print(graph.incidentEdges(nodeC))