import ast
import re
from graph import Graph 
from node import Node, Question
from typing import Dict,Tuple,List
from collections import defaultdict
import networkx as nx
import numpy as np
import random
import math
import subprocess

def skillTree(): 
        '''returns nx graph'''

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
        SKILL_TOPIC_LIST = [
        add, add_sub, time, seq, seq_n, mul, div, mul_div,
        sqr_root, sqr_surd, mixed, conversion, linear, linear_2d,
        roots, diff, diff_2
        ]
        return SKILL_TREE, SKILL_TOPIC_LIST

SKILL_TREE : nx.Graph = skillTree()[0]
SKILL_TOPICS = skillTree()[1]

def heuristic(node1: Node, node2: Node) -> float:
        '''function that returns the estimated cost of travelling to the end (should be high if far away in the skill tree)'''
        #print("heuristic called")
        #shortest_distance = nx.shortest_path_length(SKILL_TREE, node1.topic, node2.topic)

        return abs(SKILL_TOPICS.index(node1.topic) - SKILL_TOPICS.index(node2.topic))

class ExpertGraph:
    def __init__(self, topics: str, ending: str): #skill_tree : Graph
       skillTree()
       self.topic_list = []
       self.topic_list_str = []
       self.goal_topic = ending
       print("Initializing expert")
       self.graph = self.genGraph(random.choice(topics), ending) 
       print("Done")
       self.topics_prob : Dict[str, Tuple[float,float]] = {} # maps a skill to a pair of input/output of a sigmoid graph
       self.loadTopics()
       for topic in topics:
            self.topics_prob[topic] = [2.197, 0.75]
       self.motivation = 0.5
       self.comfort = 0.5
       self.questions_complete = 0
      

    def loadTopics(self, value = 0.25):
        """Loads a baseline probability of 0.25 for all the topics once the graph has been constructed"""
        for topic in self.topic_list_str:
                self.topics_prob[topic] = [0,0.25]

    def topicDifference(self, topic1, topic2):
        """Returns the difference in the difficulties of the two topics (a result greater than 0 means that topic1 is harder)"""
        return self.topic_list_str.index(topic1) - self.topic_list_str.index(topic2)

    def updateTopic(self, topic : str, isCorrect):
            """Updates the estimated probability of the topic of the question answered depending on whether it is correct or not"""
            if topic in self.topics_prob:
                if isCorrect: self.topics_prob[topic][0] += 0.2
                else: self.topics_prob[topic][0] -= 0.2
                self.topics_prob[topic][1] = self.sigmoid(self.topics_prob[topic][0])
    
    def sigmoid(self, x) -> float:
        return 1 / (1+ math.exp(-(x-1.09861)))  
    
    def computeNodeProb(self, node : Node) -> float:
        return self.topics_prob[node.topic].second
    
    def changeItUp(self, expr : str):
        """Generates similar variants of an expression by changing the numbers in the expression. Accounts for double negatives, and avoids 0's"""
        nums = re.findall(r'-?\d+',expr)
        lis = []
        for _ in nums:
            lis.append(random.sample([-5,-4,-3,-2,-1,1,2,3,4,5], 3))
        
        new_nums = []
        
        for i in range(len(nums)):
            new_nums.append([])
            for l in lis[i]:
                to_add = int(nums[i]) + l
                if to_add == 0: 
                    new_nums[i].append(2)  
                else:
                    new_nums[i].append(to_add)
        new_expr = [expr for i in range(3)]
        for j in range(3):
            for i in range(len(nums)):
                # print(new_nums[i][j])
                # print("im replacing " + nums[i] + " with " + str(new_nums[i][j]))
                new_expr[j] = re.sub(r'(?<!\d){}(?!\d)'.format(re.escape(nums[i])), str(new_nums[i][j]), new_expr[j], 1)
                #new_expr[j] = new_expr[j].replace(nums[i], str(new_nums[i][j]), 1)]
                new_expr[j] = new_expr[j].replace(" - -", " + ")

        return new_expr
    
    def skillTree(self) -> Graph:
        graph = Graph({})
        add = Node(key = "add_or_sub", name = "Addition OR Subtraction")
        add_sub = Node(key = "add_sub_multiple", name = "Addition AND Subtraction")
        time = Node(key = "time", name = "Time calculations")
        seq = Node(key="sequence_next_term", name = "Finding a sequence's next term")
        seq_n = Node(key = "sequence_nth_term", name = "Finding the nth term of a sequence")
        mul = Node(key = "mul", name= "Multiplication")
        div = Node(key = "div", name= "Division")
        mul_div = Node(key = "mul_div_multiple", name= "Multipication and Division")
        sqr_root = Node(key = "nearest_integer_root", name = "Finding the square root")
        sqr_surd = Node(key = "simplify_surd", name = "Solving expressions with square root")
        mixed = Node(key="mixed", name = "Combination of all types of arithmetic")
        conversion = Node(key = "conversion", name = "Unit conversion")
        linear = Node(key = "linear_1d", name = "Solving linear equations")
        linear_2d = Node(key = "linear_2d", name = "Solving 2d linear equations")
        roots = Node(key = "polynomial_roots", name = "Finding the roots of polynomials")
        diff = Node(key = "differentiate", name = "Finding the first derivative")
        diff_2 = Node(key = "differentiate_composed", name = "Finding more advanced derivatives (second, third, etc.)")
        
        self.topic_list = [
        add, add_sub, time, seq, seq_n, mul, div, mul_div,
        sqr_root, sqr_surd, mixed, conversion, linear, linear_2d,
        roots, diff, diff_2
        ]
        
        self.topic_list_str = [
        add.key, add_sub.key, conversion.key, time.key, seq.key, seq_n.key, mul.key, div.key, mul_div.key,
        sqr_root.key, mixed.key, linear.key, linear_2d.key, sqr_surd.key,
        roots.key, diff.key, diff_2.key
        ]

        graph.createEdge(add, add_sub, 1)
        graph.createEdge(add, time, 1)
        graph.createEdge(add_sub, seq, 1)
        graph.createEdge(seq, seq_n, 1)
        graph.createEdge(add_sub, mul, 1)
        graph.createEdge(add_sub, div, 1)
        graph.createEdge(mul, mul_div, 1)
        graph.createEdge(div, mul_div, 1)
        graph.createEdge(mul_div, mixed, 1)
        graph.createEdge(mul_div, sqr_root, 1)
        graph.createEdge(sqr_root, sqr_surd, 1)
        graph.createEdge(mul_div, linear, 1)
        graph.createEdge(mul_div, conversion, 1)
        graph.createEdge(linear, linear_2d, 1)
        graph.createEdge(linear, roots, 1)
        graph.createEdge(linear_2d, diff, 1)
        graph.createEdge(roots, diff, 1)
        graph.createEdge(diff, diff_2, 1)

        return graph

    def genGraph(self, starting_topic : str, ending_topic : str):
        print(f"Starting topic is {starting_topic}. Ending topic is {ending_topic}")

        graph = Graph({})
        skill_tree : Graph = self.skillTree()
        count = 1
        end_count = 0

        for topic in self.topic_list:
            if topic.key == starting_topic: starting_topic_node = topic

        starting_node = Node(key = f'{count}, {starting_topic}', topic = starting_topic, question= self.genQuestion(topic= starting_topic))
        self.curr = starting_node
        self.end = None
        topic_queue = []
        node_queue = []
        topic_queue.append(starting_topic_node)
        node_queue.append(starting_node)
        topic_seen = defaultdict(int)
        reached_end = False
        while((count < 20 or not reached_end)):
            if not node_queue: break
            curr_node = node_queue.pop(-1)
            curr_topic = topic_queue.pop(-1)
            for _ in range(1): 
                the_list = list(skill_tree.incidentEdges(curr_topic).keys())
                random.shuffle(the_list)
                for adj_topic in the_list:
                      if topic_seen[adj_topic] > 10:
                          continue
                      topic_seen[adj_topic] += 1
                      count+=1
                      new_node = Node(key = f'{count}, {adj_topic.key}', topic = adj_topic.key, question = self.genQuestion(adj_topic.key)) #cant have keys being identical
                      graph.createEdge(curr_node, new_node, 1)
                      print(f'comparing {adj_topic.key} with {ending_topic}')
                      if adj_topic.key == ending_topic: 
                        reached_end = True
                        print("I reached this condition check")
                        self.end = new_node
                        end_count += 1                    
                      topic_queue.append(adj_topic)
                      node_queue.append(new_node)
        node_list = list(graph.G.nodes())
        for node in graph.G.nodes():
            random_node = random.choice(node_list)
            if node.key is not random_node.key and not graph.G.has_edge(node, random_node) and nx.shortest_path_length(SKILL_TREE, random_node.topic, node.topic) <= 1:
                graph.createEdge(node, random_node, 1)
    
        return graph
      

    def genQuestion(self, topic : str):  
        """Generates a question of a given topic returning a Question object"""
        result = subprocess.getoutput(f'python -m mathematics_dataset.generate --filter={topic} --per_train_module=1 --per_test_module=1')
        result = result.replace("\n", "")
        result = result[result.find("["):]
        #print(f"Result: {topic}")
        #print(result)
        qa_pairs = ast.literal_eval(result)
        pair = qa_pairs[0]
        question = pair[0].strip()
        answer : str = pair[1].strip()
        
        #print(f"Question: {question}")
        #print(f"Answer: {answer}")

        options = self.changeItUp(answer)
        options.append(answer)
        random.shuffle(options)
        #ans = int(answer)
        
        return Question(question, options, answer)
      
    def nextQuestion(self) -> Node:
        #TODO: create a class variable curr node that keeps track of where we are at
        if self.end is None: print("END IS NONE")
        # for neighbor in self.graph.G.neighbors(self.curr):
        print("astar start")
        print(f"Current node: {self.curr}, End node: {self.end}")
        if self.curr is None or self.end is None: ValueError("Current or End node is None!")
        #next_node = (nx.astar_path(self.graph.G, self.curr, self.end, heuristic = lambda u, v: heuristic(u,v)))[1]
        #short_path = nx.shortest_path(self.graph.G, self.curr, self.end, weight = "weight")
        short_path = nx.astar_path(self.graph.G, self.curr, self.end, heuristic = lambda u, v: heuristic(u,v), weight = "weight")
        self.questions_complete = self.questions_complete + 1
        if len(short_path) <= 1:
            return random.choice(list(self.graph.vertexList.keys()))
        self.curr = short_path[1]
        return short_path[1]
        
        # randomNode : Node = random.choice(list(self.graph.vertexList.keys()))
        # self.questions_complete = self.questions_complete + 1
        # print(self.topics_prob[randomNode.topic][1])
        # return randomNode

    def availableQuestions(self):
        '''returns if the user has mastered a goal (considered to be the probability their predicted success is greater than a "req_val" a threshold determined by the motivation & comfort)'''
        if self.motivation > 0.5 : 
            req_val = 0.65
            if self.comfort > 0.5 : 
                req_val = 0.5
        else: req_val = 0.75 
        return self.topics_prob[self.goal_topic][1] < req_val
        #return self.questions_complete < len(self.graph.vertexList.keys())
    
    def updateViability(self):
        G = self.graph.G
        
        #handle the case where the comfort is pretty low
        
        for u, v, data in G.edges(data = True):
            curr_score = data.get('weight', 0)
            diff = nx.shortest_path_length(SKILL_TREE, u.topic, v.topic)
            curr_score += (1 - self.motivation) * 5 * diff
            curr_score += (1 - self.comfort) * 5 * ((self.topics_prob[u.topic][1] - self.topics_prob[v.topic][1] + 1) / 2 )

            self.graph.updateEdge(u,v, curr_score)

    


# curr_node = Node()


