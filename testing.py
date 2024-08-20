import random
import subprocess
import ast
import re
import time
import networkx as nx
import numpy as np
from learning import ExpertGraph

def skillTree():
        graph = nx.Graph()

        add = "add_or_sub"
        add_sub = "add_sub_multiple"
        time = "time"
        seq ="sequence_next_term"
        seq_n = "sequence_nth_term"
        mul = "mul"
        div = "div"
        mul_div = "mul_div_multiple"
        sqr_root ="nearest_integer_root"
        sqr_surd = "simplify_surd"
        mixed = "mixed"
        conversion = "conversion"
        linear ="linear_1d"
        linear_2d = "linear_2d"
        roots = "polynomial_roots"
        diff = "differentiate"
        diff_2 = "differentiate_composed"

        graph.add_edge(add, add_sub, weight = 1)
        graph.add_edge(add, time, weight = 1)
        graph.add_edge(add_sub, seq, weight = 1)
        graph.add_edge(seq, seq_n, weight = 1)
        graph.add_edge(add_sub, mul, weight = 1)
        graph.add_edge(add_sub, div, weight = 1)
        graph.add_edge(mul, mul_div, weight = 1)
        graph.add_edge(div, mul_div, weight = 1)
        graph.add_edge(mul_div, mixed, weight = 1)
        graph.add_edge(mul_div, sqr_root, weight = 1)
        graph.add_edge(sqr_root, sqr_surd, weight = 1)
        graph.add_edge(mul_div, linear, weight = 1)
        graph.add_edge(mul_div, conversion, weight = 1)
        graph.add_edge(linear, linear_2d, weight = 1)
        graph.add_edge(linear, roots, weight = 1)
        graph.add_edge(linear_2d, diff, weight = 1)
        graph.add_edge(roots, diff, weight = 1)
        graph.add_edge(diff, diff_2, weight = 1)

        SKILL_TREE = graph

        return SKILL_TREE

def heuristic(str1, str2) -> float:
        '''function that returns the estimated cost of travelling to the end (should be high if far away in the skill tree)'''
        SKILL_TREE = skillTree()
    
        shortest_distance = nx.shortest_path_length(SKILL_TREE, str1, str2)
        return shortest_distance

print(heuristic("differentiate", "differentiate"))

