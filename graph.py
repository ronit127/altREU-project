from typing import Dict, List
from node import Node

class Edge:

    def __init__(self, node1: Node, node2: Node, viable_score: float):
        self.node1 = node1
        self.node2 = node2
        self.viable_score = viable_score


class Graph:
    
    #load nodes                                   #other node
    def __init__(self, vertexList: Dict[Node, Dict[Node, Edge]]):
        self.vertexList = vertexList

    def createEdge(self, node1 : Node, node2: Node, viable_score: float):
        new_edge = Edge(node1, node2, viable_score)
        self.vertexList[node1][node2] = new_edge
        self.vertexList[node2][node1] = new_edge 
    
    def updateEdge(self, node1: Node, node2: Node, new_score: float):
        self.vertexList[node1][node2].viable_score = new_score
        self.vertexList[node2][node1].viable_score = new_score

    def incidentEdges(self, node: Node) -> Dict[Node, Edge]:
        return self.vertexList[node]
        


